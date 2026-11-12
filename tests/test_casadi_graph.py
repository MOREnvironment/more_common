from types import SimpleNamespace

import casadi as ca
import numpy as np

from more_common.casadi_graph import RppCasadiGraph, graph_from_bytes, graph_to_bytes


def test_serialized_graph_retains_vector_computation():
    value = ca.SX.sym("value", 2)
    graph = ca.Function("affine", [value], [2 * value + ca.DM([1, -3])])

    restored = graph_from_bytes(graph_to_bytes(graph))

    np.testing.assert_allclose(np.asarray(restored([4, 5])).ravel(), [9, 7])


def test_payload_retains_dynamics_and_independent_vector_offsets():
    state = ca.SX.sym("state", 2)
    command = ca.SX.sym("command")
    output = ca.Function("output", [state, command], [state[0]])
    step = ca.Function("step", [state, command], [ca.vertcat(state[1], command)])
    payload = SimpleNamespace(
        output=graph_to_bytes(output),
        dynamics=graph_to_bytes(step),
        inputDescription=[SimpleNamespace(size=1)],
        stateDescription=[SimpleNamespace(size=2)],
        outputDescription=[SimpleNamespace(size=1)],
    )

    graph = RppCasadiGraph(payload, 3, 7, 11)

    assert graph.slice_input() == slice(3, 4)
    assert graph.slice_state() == slice(7, 9)
    assert graph.slice_output() == slice(11, 12)
    np.testing.assert_allclose(np.asarray(graph.step([4, 5], 6)).ravel(), [5, 6])


def test_output_only_payload_has_no_dynamics():
    value = ca.SX.sym("value")
    payload = SimpleNamespace(
        output=graph_to_bytes(ca.Function("identity", [value], [value])),
        dynamics=b"",
        inputDescription=[],
        stateDescription=[],
        outputDescription=[SimpleNamespace(size=1)],
    )

    assert RppCasadiGraph(payload).step is None
