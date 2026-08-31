from typing import Any

import casadi as ca


class RppCasadiGraph:
    def __init__(
        self,
        payload: Any,
        start_index_input: int = 0,
        start_index_state: int = 0,
        start_index_output: int = 0,
    ) -> None:
        self.payload = payload
        self.output = graph_from_bytes(payload.output)
        self.step = (
            graph_from_bytes(payload.dynamics)
            if payload.dynamics
            else None
        )
        self.num_inputs = sum(desc.size for desc in payload.inputDescription)
        self.num_states = sum(desc.size for desc in payload.stateDescription)
        self.num_outputs = sum(desc.size for desc in payload.outputDescription)
        self.start_index_input = start_index_input
        self.start_index_state = start_index_state
        self.start_index_output = start_index_output
        self.end_index_input = start_index_input + self.num_inputs
        self.end_index_state = start_index_state + self.num_states
        self.end_index_output = start_index_output + self.num_outputs

    def slice_input(self) -> slice:
        return slice(self.start_index_input, self.end_index_input)

    def slice_state(self) -> slice:
        return slice(self.start_index_state, self.end_index_state)

    def slice_output(self) -> slice:
        return slice(self.start_index_output, self.end_index_output)


def graph_from_bytes(graph_bytes: bytes) -> ca.Function:
    """Deserialize a CasADi function from an RPP payload."""
    return ca.Function.deserialize(graph_bytes.decode("utf-8"))


def graph_to_bytes(graph: ca.Function) -> bytes:
    """Serialize a CasADi function for an RPP payload."""
    return graph.serialize().encode("utf-8")
