import pytest
from _pytest.terminal import TerminalReporter
import time
from collections import Counter
import inspect


def pytest_collection_modifyitems(config, items):
    for item in items:
        node = item.obj
        node_parts = item.nodeid.split("::")
        node_str = node.__doc__ or node_parts[-1]
        item._nodeid = node_str


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    vanilla_reporter = config.pluginmanager.getplugin("terminalreporter")
    my_reporter = MyReporter(config)
    config.pluginmanager.unregister(vanilla_reporter)
    config.pluginmanager.register(my_reporter, "terminalreporter")


class MyReporter(TerminalReporter):
    def __init__(self, config, file=None):
        TerminalReporter.__init__(self, config, file)
        self._last_header = None

    def short_test_summary(self):
        # your own impl goes here, for example:
        self.write_sep("=", "my own short summary info")
        failed = self.stats.get("failed", [])
        for rep in failed:
            self.write_line(f"{rep.nodeid}")

    # @pytest.hookimpl(hookwrapper=True)
    def pytest_terminal_summary(self):
        self.short_test_summary()
        pass

    def pytest_sessionstart(self, session):
        self._session = session
        self._sessionstarttime = time.time()
        pass

    def _get_progress_information_message(self):
        assert self._session
        collected = self._session.testscollected
        if collected:
            return " [{:3d}%]".format(
                len(self._progress_nodeids_reported) * 100 // collected
            )
        return " [100%]"

    @pytest.hookimpl(hookwrapper=True)
    def pytest_sessionfinish(self, session, exitstatus):
        yield

    def pytest_runtest_logreport(self, report):
        self._tests_ran = True
        rep = report
        res = self.config.hook.pytest_report_teststatus(report=rep, config=self.config)
        category, letter, word = res
        if not isinstance(word, tuple):
            markup = None
        else:
            word, markup = word
        self._add_stats(category, [rep])
        if not letter and not word:
            # Probably passed setup/teardown.
            return
        running_xdist = hasattr(rep, "node")
        if markup is None:
            was_xfail = hasattr(report, "wasxfail")
            if rep.passed and not was_xfail:
                markup = {"green": True}
            elif rep.passed and was_xfail:
                markup = {"yellow": True}
            elif rep.failed:
                markup = {"red": True}
            elif rep.skipped:
                markup = {"yellow": True}
            else:
                markup = {}
        if self.verbosity <= 0:
            self._tw.write(letter, **markup)
        else:
            self._progress_nodeids_reported.add(rep.nodeid)
            line = self._locationline(rep.nodeid, *rep.location)
            if not running_xdist:
                self.write_ensure_prefix(line, word, **markup)
                if rep.skipped or hasattr(report, "wasxfail"):
                    reason = _get_raw_skip_reason(rep)
                    if self.config.option.verbose < 2:
                        available_width = (
                            (self._tw.fullwidth - self._tw.width_of_current_line)
                            - len(" [100%]")
                            - 1
                        )
                        formatted_reason = _format_trimmed(
                            " ({})", reason, available_width
                        )
                    else:
                        formatted_reason = f" ({reason})"

                    if reason and formatted_reason is not None:
                        self._tw.write(formatted_reason)
                if self._show_progress_info:
                    self._write_progress_information_filling_space()
            else:
                self.ensure_newline()
                self._tw.write("[%s]" % rep.node.gateway.id)
                if self._show_progress_info:
                    self._tw.write(
                        self._get_progress_information_message() + " ", cyan=True
                    )
                else:
                    self._tw.write(" ")
                self._tw.write(word, **markup)
                self._tw.write(" " + line)
                self.currentfspath = -2
        self.flush()
