import contextlib
import io
import sys
import pytest

import psyneulink as pnl
from psyneulink.core.compositions.report import ReportOutput, ReportDevices


class TestReport():

    @pytest.mark.skipif(sys.platform == 'win32', reason="<Incompatible UDF-8 formatting of rich Console output>")
    def test_simple_output_and_progress(self):
        """Test simple sequence of three Mechanisms, using all report_output and report_progress options
        """
        a = pnl.TransferMechanism(name='a')
        b = pnl.TransferMechanism(name='b')
        c = pnl.TransferMechanism(name='c')
        comp = pnl.Composition(pathways=[a,b,c], name='COMP')

        a.reportOutputPref=ReportOutput.FULL
        b.reportOutputPref=ReportOutput.OFF
        c.reportOutputPref=ReportOutput.FULL

        comp.run(report_output=ReportOutput.TERSE, report_to_devices=ReportDevices.DIVERT)
        actual_output = comp.rich_diverted_reports
        expected_output = '\'\\nCOMP TRIAL 0 ====================\\n Time Step 0 ---------\\n  a executed\\n Time Step 1 ---------\\n  b executed\\n Time Step 2 ---------\\n  c executed\\n\''
        assert repr(actual_output) == expected_output

        comp.run(report_output=ReportOutput.TERSE, report_progress=True, report_to_devices=ReportDevices.DIVERT)
        actual_output = comp.rich_diverted_reports
        expected_output = '\nCOMP TRIAL 0 ====================\n Time Step 0 ---------\n  a executed\n Time Step 1 ---------\n  b executed\n Time Step 2 ---------\n  c executed\nCOMP: Executed 1 of 1 trials\n'
        assert actual_output == expected_output

        comp.run(report_output=ReportOutput.USE_PREFS, report_to_devices=ReportDevices.DIVERT)
        actual_output = comp.rich_diverted_reports
        expected_output = '\nCOMP TRIAL 0 ====================\n Time Step 0 ---------\n╭───── a ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\n Time Step 1 ---------\n Time Step 2 ---------\n╭───── c ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\n'
        assert actual_output == expected_output

        comp.run(report_output=ReportOutput.USE_PREFS, report_progress=True, report_to_devices=ReportDevices.DIVERT)
        actual_output = comp.rich_diverted_reports
        expected_output = '\nCOMP TRIAL 0 ====================\n Time Step 0 ---------\n╭───── a ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\n Time Step 1 ---------\n Time Step 2 ---------\n╭───── c ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\nCOMP: Executed 1 of 1 trials\n'
        assert actual_output == expected_output

        comp.run(report_output=ReportOutput.FULL, report_to_devices=ReportDevices.DIVERT)
        actual_output = comp.rich_diverted_reports
        expected_output = '\n┏━━  COMP: Trial 0  ━━┓\n┃                     ┃\n┃ input: [[0.0]]      ┃\n┃                     ┃\n┃ ┌─  Time Step 0 ──┐ ┃\n┃ │ ╭───── a ─────╮ │ ┃\n┃ │ │ input: 0.0  │ │ ┃\n┃ │ │ output: 0.0 │ │ ┃\n┃ │ ╰─────────────╯ │ ┃\n┃ └─────────────────┘ ┃\n┃                     ┃\n┃ ┌─  Time Step 1 ──┐ ┃\n┃ │ ╭───── b ─────╮ │ ┃\n┃ │ │ input: 0.0  │ │ ┃\n┃ │ │ output: 0.0 │ │ ┃\n┃ │ ╰─────────────╯ │ ┃\n┃ └─────────────────┘ ┃\n┃                     ┃\n┃ ┌─  Time Step 2 ──┐ ┃\n┃ │ ╭───── c ─────╮ │ ┃\n┃ │ │ input: 0.0  │ │ ┃\n┃ │ │ output: 0.0 │ │ ┃\n┃ │ ╰─────────────╯ │ ┃\n┃ └─────────────────┘ ┃\n┃                     ┃\n┃ result: [[0.0]]     ┃\n┃                     ┃\n┗━━━━━━━━━━━━━━━━━━━━━┛\n\n'
        assert actual_output == expected_output

        comp.run(report_output=ReportOutput.FULL, report_progress=True, report_to_devices=ReportDevices.DIVERT)
        actual_output = comp.rich_diverted_reports
        expected_output = '\n┏━━  COMP: Trial 0  ━━┓\n┃                     ┃\n┃ input: [[0.0]]      ┃\n┃                     ┃\n┃ ┌─  Time Step 0 ──┐ ┃\n┃ │ ╭───── a ─────╮ │ ┃\n┃ │ │ input: 0.0  │ │ ┃\n┃ │ │ output: 0.0 │ │ ┃\n┃ │ ╰─────────────╯ │ ┃\n┃ └─────────────────┘ ┃\n┃                     ┃\n┃ ┌─  Time Step 1 ──┐ ┃\n┃ │ ╭───── b ─────╮ │ ┃\n┃ │ │ input: 0.0  │ │ ┃\n┃ │ │ output: 0.0 │ │ ┃\n┃ │ ╰─────────────╯ │ ┃\n┃ └─────────────────┘ ┃\n┃                     ┃\n┃ ┌─  Time Step 2 ──┐ ┃\n┃ │ ╭───── c ─────╮ │ ┃\n┃ │ │ input: 0.0  │ │ ┃\n┃ │ │ output: 0.0 │ │ ┃\n┃ │ ╰─────────────╯ │ ┃\n┃ └─────────────────┘ ┃\n┃                     ┃\n┃ result: [[0.0]]     ┃\n┃                     ┃\n┗━━━━━━━━━━━━━━━━━━━━━┛\n\nCOMP: Executed 1 of 1 trials\n'
        assert actual_output == expected_output

        # Run these tests after ones calling run() above to avoid having to reset trial counter,
        # which increments after calls to execute()
        comp.execute(report_output=ReportOutput.TERSE, report_to_devices=ReportDevices.DIVERT)
        actual_output = comp.rich_diverted_reports
        expected_output = '\'\\nCOMP TRIAL 0 ====================\\n Time Step 0 ---------\\n  a executed\\n Time Step 1 ---------\\n  b executed\\n Time Step 2 ---------\\n  c executed\\n\''
        assert repr(actual_output) == expected_output

        comp.execute(report_output=ReportOutput.TERSE, report_progress=True, report_to_devices=ReportDevices.DIVERT)
        actual_output = comp.rich_diverted_reports
        expected_output = '\'\\nCOMP TRIAL 1 ====================\\n Time Step 0 ---------\\n  a executed\\n Time Step 1 ---------\\n  b executed\\n Time Step 2 ---------\\n  c executed\\n[red]Executing COMP...\\n\''
        assert repr(actual_output) == expected_output

        comp.execute(report_output=ReportOutput.USE_PREFS, report_to_devices=ReportDevices.DIVERT)
        actual_output = comp.rich_diverted_reports
        expected_output = '\nCOMP TRIAL 2 ====================\n Time Step 0 ---------\n╭───── a ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\n Time Step 1 ---------\n Time Step 2 ---------\n╭───── c ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\n'
        assert actual_output == expected_output

        comp.execute(report_output=ReportOutput.USE_PREFS, report_progress=True, report_to_devices=ReportDevices.DIVERT)
        actual_output = comp.rich_diverted_reports
        expected_output = '\nCOMP TRIAL 3 ====================\n Time Step 0 ---------\n╭───── a ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\n Time Step 1 ---------\n Time Step 2 ---------\n╭───── c ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\n[red]Executing COMP...\n'
        assert actual_output == expected_output

        comp.execute(report_output=ReportOutput.FULL, report_to_devices=ReportDevices.DIVERT)
        actual_output = comp.rich_diverted_reports
        expected_output = '\n┏━━  COMP: Trial 4  ━━┓\n┃                     ┃\n┃ input: [[0.0]]      ┃\n┃                     ┃\n┃ ┌─  Time Step 0 ──┐ ┃\n┃ │ ╭───── a ─────╮ │ ┃\n┃ │ │ input: 0.0  │ │ ┃\n┃ │ │ output: 0.0 │ │ ┃\n┃ │ ╰─────────────╯ │ ┃\n┃ └─────────────────┘ ┃\n┃                     ┃\n┃ ┌─  Time Step 1 ──┐ ┃\n┃ │ ╭───── b ─────╮ │ ┃\n┃ │ │ input: 0.0  │ │ ┃\n┃ │ │ output: 0.0 │ │ ┃\n┃ │ ╰─────────────╯ │ ┃\n┃ └─────────────────┘ ┃\n┃                     ┃\n┃ ┌─  Time Step 2 ──┐ ┃\n┃ │ ╭───── c ─────╮ │ ┃\n┃ │ │ input: 0.0  │ │ ┃\n┃ │ │ output: 0.0 │ │ ┃\n┃ │ ╰─────────────╯ │ ┃\n┃ └─────────────────┘ ┃\n┃                     ┃\n┃ result: [[0.0]]     ┃\n┃                     ┃\n┗━━━━━━━━━━━━━━━━━━━━━┛\n\n'
        assert actual_output == expected_output

        comp.execute(report_output=ReportOutput.FULL, report_progress=True, report_to_devices=ReportDevices.DIVERT)
        actual_output = comp.rich_diverted_reports
        expected_output = '\n┏━━  COMP: Trial 5  ━━┓\n┃                     ┃\n┃ input: [[0.0]]      ┃\n┃                     ┃\n┃ ┌─  Time Step 0 ──┐ ┃\n┃ │ ╭───── a ─────╮ │ ┃\n┃ │ │ input: 0.0  │ │ ┃\n┃ │ │ output: 0.0 │ │ ┃\n┃ │ ╰─────────────╯ │ ┃\n┃ └─────────────────┘ ┃\n┃                     ┃\n┃ ┌─  Time Step 1 ──┐ ┃\n┃ │ ╭───── b ─────╮ │ ┃\n┃ │ │ input: 0.0  │ │ ┃\n┃ │ │ output: 0.0 │ │ ┃\n┃ │ ╰─────────────╯ │ ┃\n┃ └─────────────────┘ ┃\n┃                     ┃\n┃ ┌─  Time Step 2 ──┐ ┃\n┃ │ ╭───── c ─────╮ │ ┃\n┃ │ │ input: 0.0  │ │ ┃\n┃ │ │ output: 0.0 │ │ ┃\n┃ │ ╰─────────────╯ │ ┃\n┃ └─────────────────┘ ┃\n┃                     ┃\n┃ result: [[0.0]]     ┃\n┃                     ┃\n┗━━━━━━━━━━━━━━━━━━━━━┛\n\n[red]Executing COMP...\n'
        assert actual_output == expected_output

    # def test_two_mechs_in_a_time_step(self):
    #     """Test that includes two (recurrently connected) Mechanisms executed within the same TIME_STEP
    #        FIX: NEED TO RESOLVE INDETERMINACY OF ORDER OF EXECUTION FOR TESTING
    #     """
    #     a = TransferMechanism(name='a')
    #     b = TransferMechanism(name='b')
    #     c = TransferMechanism(name='c')
    #     comp = Composition(pathways=[[a,b],[b,a], [a,c]], name='COMP')
    #
    #     a.reportOutputPref=True
    #     b.reportOutputPref=False
    #     c.reportOutputPref=True
    #
    #     comp.run(report_output=TERSE, report_progress=[False, ReportDevices.DIVERT])
    #     actual_output = comp.rich_diverted_reports
    #     expected_output = '\nCOMP TRIAL 0 ====================\n Time Step 0 ---------\n  a executed\n  b executed\n Time Step 1 ---------\n  c executed\n\nCOMP TRIAL 0 ====================\n Time Step 0 ---------\n  a executed\n  b executed\n Time Step 1 ---------\n  c executed\nCOMP TRIAL 1 ====================\n Time Step 0 ---------\n  a executed\n  b executed\n Time Step 1 ---------\n  c executed\n'
    #     assert actual_output == expected_output
    #
    #     comp.run(report_output=TERSE, report_progress=ReportDevices.DIVERT)
    #     actual_output = comp.rich_diverted_reports
    #     expected_output = '\nCOMP TRIAL 0 ====================\n Time Step 0 ---------\n  b executed\n  a executed\n Time Step 1 ---------\n  c executed\nCOMP: Executed 1 of 2 trials\nCOMP TRIAL 0 ====================\n Time Step 0 ---------\n  b executed\n  a executed\n Time Step 1 ---------\n  c executed\nCOMP TRIAL 1 ====================\n Time Step 0 ---------\n  b executed\n  a executed\n Time Step 1 ---------\n  c executed\nCOMP: Executed 2 of 2 trials'
    #     assert actual_output == expected_output
    #
    #     comp.run(report_output=True, report_progress=ReportDevices.DIVERT)
    #     actual_output = comp.rich_diverted_reports
    #     expected_output = '\nCOMP TRIAL 0 ====================\n Time Step 0 ---------\n╭───── a ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\n Time Step 1 ---------\n╭───── c ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\nCOMP: Executed 1 of 2 trials\nCOMP TRIAL 0 ====================\n Time Step 0 ---------\n╭───── a ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\n Time Step 1 ---------\n╭───── c ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\nCOMP TRIAL 1 ====================\n Time Step 0 ---------\n╭───── a ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\n Time Step 1 ---------\n╭───── c ─────╮\n│ input: 0.0  │\n│ output: 0.0 │\n╰─────────────╯\nCOMP: Executed 2 of 2 trials'
    #     assert actual_output == expected_output
    #
    #     comp.run(num_trials=2, report_output=FULL, report_progress=ReportDevices.DIVERT)
    #     actual_output = comp.rich_diverted_reports
    #     expected_output = '\n┏━━━  COMP: Trial 0  ━━━┓\n┃                       ┃\n┃ input: [[0.0], [0.0]] ┃\n┃                       ┃\n┃ ┌─  Time Step 0 ──┐   ┃\n┃ │ ╭───── b ─────╮ │   ┃\n┃ │ │ input: 0.0  │ │   ┃\n┃ │ │ output: 0.0 │ │   ┃\n┃ │ ╰─────────────╯ │   ┃\n┃ │ ╭───── a ─────╮ │   ┃\n┃ │ │ input: 0.0  │ │   ┃\n┃ │ │ output: 0.0 │ │   ┃\n┃ │ ╰─────────────╯ │   ┃\n┃ └─────────────────┘   ┃\n┃                       ┃\n┃ ┌─  Time Step 1 ──┐   ┃\n┃ │ ╭───── c ─────╮ │   ┃\n┃ │ │ input: 0.0  │ │   ┃\n┃ │ │ output: 0.0 │ │   ┃\n┃ │ ╰─────────────╯ │   ┃\n┃ └─────────────────┘   ┃\n┃                       ┃\n┃ result: [[0.0]]       ┃\n┃                       ┃\n┗━━━━━━━━━━━━━━━━━━━━━━━┛\n\nCOMP: Executed 1 of 2 trials\n┏━━━  COMP: Trial 0  ━━━┓\n┃                       ┃\n┃ input: [[0.0], [0.0]] ┃\n┃                       ┃\n┃ ┌─  Time Step 0 ──┐   ┃\n┃ │ ╭───── b ─────╮ │   ┃\n┃ │ │ input: 0.0  │ │   ┃\n┃ │ │ output: 0.0 │ │   ┃\n┃ │ ╰─────────────╯ │   ┃\n┃ │ ╭───── a ─────╮ │   ┃\n┃ │ │ input: 0.0  │ │   ┃\n┃ │ │ output: 0.0 │ │   ┃\n┃ │ ╰─────────────╯ │   ┃\n┃ └─────────────────┘   ┃\n┃                       ┃\n┃ ┌─  Time Step 1 ──┐   ┃\n┃ │ ╭───── c ─────╮ │   ┃\n┃ │ │ input: 0.0  │ │   ┃\n┃ │ │ output: 0.0 │ │   ┃\n┃ │ ╰─────────────╯ │   ┃\n┃ └─────────────────┘   ┃\n┃                       ┃\n┃ result: [[0.0]]       ┃\n┃                       ┃\n┗━━━━━━━━━━━━━━━━━━━━━━━┛\n\n┏━━━  COMP: Trial 1  ━━━┓\n┃                       ┃\n┃ input: [[0.0], [0.0]] ┃\n┃                       ┃\n┃ ┌─  Time Step 0 ──┐   ┃\n┃ │ ╭───── b ─────╮ │   ┃\n┃ │ │ input: 0.0  │ │   ┃\n┃ │ │ output: 0.0 │ │   ┃\n┃ │ ╰─────────────╯ │   ┃\n┃ │ ╭───── a ─────╮ │   ┃\n┃ │ │ input: 0.0  │ │   ┃\n┃ │ │ output: 0.0 │ │   ┃\n┃ │ ╰─────────────╯ │   ┃\n┃ └─────────────────┘   ┃\n┃                       ┃\n┃ ┌─  Time Step 1 ──┐   ┃\n┃ │ ╭───── c ─────╮ │   ┃\n┃ │ │ input: 0.0  │ │   ┃\n┃ │ │ output: 0.0 │ │   ┃\n┃ │ ╰─────────────╯ │   ┃\n┃ └─────────────────┘   ┃\n┃                       ┃\n┃ result: [[0.0]]       ┃\n┃                       ┃\n┗━━━━━━━━━━━━━━━━━━━━━━━┛\n\nCOMP: Executed 2 of 2 trials'
    #     assert actual_output == expected_output

    # def test_nested_comps_output(self):
    #     """Test of nested Compositions with simulations executed by OCMs"""
    #
    #     with_inner_controller = True
    #     with_outer_controller = True
    #
    #     # instantiate mechanisms and inner comp
    #     ia = pnl.TransferMechanism(name='ia')
    #     ib = pnl.TransferMechanism(name='ib')
    #     icomp = pnl.Composition(name='icomp', controller_mode=pnl.BEFORE)
    #
    #     # set up structure of inner comp
    #     icomp.add_node(ia, required_roles=pnl.NodeRole.INPUT)
    #     icomp.add_node(ib, required_roles=pnl.NodeRole.OUTPUT)
    #     icomp.add_projection(pnl.MappingProjection(), sender=ia, receiver=ib)
    #
    #     # add controller to inner comp
    #     if with_inner_controller:
    #         icomp.add_controller(
    #                 pnl.OptimizationControlMechanism(
    #                         agent_rep=icomp,
    #                         features=[ia.input_port],
    #                         name="iController",
    #                         objective_mechanism=pnl.ObjectiveMechanism(
    #                                 monitor=ib.output_port,
    #                                 function=pnl.SimpleIntegrator,
    #                                 name="iController Objective Mechanism"
    #                         ),
    #                         function=pnl.GridSearch(direction=pnl.MAXIMIZE),
    #                         control_signals=[pnl.ControlSignal(projections=[(pnl.SLOPE, ia)],
    #                                                            variable=1.0,
    #                                                            intensity_cost_function=pnl.Linear(slope=0.0),
    #                                                            allocation_samples=pnl.SampleSpec(start=1.0,
    #                                                                                              stop=10.0,
    #                                                                                              num=4))])
    #         )
    #
    #     # instantiate outer comp
    #     ocomp = pnl.Composition(name='ocomp', controller_mode=pnl.BEFORE)
    #
    #     # setup structure of outer comp
    #     ocomp.add_node(icomp)
    #
    #     ocomp._analyze_graph()
    #
    #     # add controller to outer comp
    #     if with_outer_controller:
    #         ocomp.add_controller(
    #                 pnl.OptimizationControlMechanism(
    #                         agent_rep=ocomp,
    #                         # features=[ia.input_port],
    #                         features=[ocomp.input_CIM.output_ports[0]],
    #                         name="oController",
    #                         objective_mechanism=pnl.ObjectiveMechanism(
    #                                 monitor=ib.output_port,
    #                                 function=pnl.SimpleIntegrator,
    #                                 name="oController Objective Mechanism"
    #                         ),
    #                         function=pnl.GridSearch(direction=pnl.MAXIMIZE),
    #                         control_signals=[pnl.ControlSignal(projections=[(pnl.SLOPE, ia)],
    #                                                            variable=1.0,
    #                                                            intensity_cost_function=pnl.Linear(slope=0.0),
    #                                                            allocation_samples=pnl.SampleSpec(start=1.0,
    #                                                                                              stop=10.0,
    #                                                                                              num=3))])
    #         )
    #
    #     inputs_dict = {
    #         icomp:
    #             {
    #                 ia: [[-2], [1]]
    #             }
    #     }
    #
    #     def inputs_generator_function():
    #         for i in range(2):
    #             yield {
    #                 icomp:
    #                     {
    #                         ia: inputs_dict[icomp][ia][i]
    #                     }
    #             }
    #
    #     inputs_generator_instance = inputs_generator_function()
    #
    #     # ocomp.run(inputs=inputs_generator_function)
    #     # ocomp.run(inputs=inputs_generator_instance, report_progress=['simulations'])
    #     # ocomp.run(inputs=inputs_dict, report_progress=True)
    #     # ocomp.run(inputs=inputs_dict, report_progress=['simulations'])
    #
    #     ocomp.run(inputs={icomp:-2}, report_output=FULL, report_simulations=True, report_to_devices=ReportDevices.DIVERT)
    #     actual_output = ocomp.rich_diverted_reports
    #     expected_output = '\nocomp TRIAL 0 ====================\n Time Step 0 ---------\nicomp TRIAL 0 ====================\n Time Step 0 ---------\n Time Step 0 ---------\n Time Step 0 ---------\n Time Step 1 ---------\nocomp: Executed 1 of 1 trials\nocomp: Simulated 3 trials\nicomp: Executed 1 of 1 trials\nicomp: Simulated 4 trials\nicomp: Executed 1 of 1 trials\nicomp: Simulated 4 trials\nicomp: Executed 1 of 1 trials\nicomp: Simulated 4 trials\nicomp: Executed 1 of 1 trials\nicomp: Simulated 4 trials'
    #     assert actual_output == expected_output

    def test_reportOutputPref_true(self):
        t = pnl.TransferMechanism()
        t.reportOutputPref = ReportOutput.FULL

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            t.execute(1)
        output = f.getvalue()

        assert 'input: 1.0' in output
        assert 'output: 1.0' in output
        assert 'params' not in output

    def test_reportOutputPref_params(self):
        t = pnl.TransferMechanism()
        t.reportOutputPref = 'params'

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            t.execute(1)
        output = f.getvalue()

        assert 'input: 1.0' in output
        assert 'output: 1.0' in output
        assert 'params' in output

        # NOTE: parameters are not consistent in printed form with
        # their underlying values (e.g. dimension brackets are removed)
        # So, don't check output for all parameters and correct values
        assert 'noise:' in output
        assert 'integration_rate:' in output

        assert 'Parameter(' not in output
        assert 'pnl_internal=' not in output
