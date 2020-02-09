from pm4py.objects.petri.utils import acyclic_net_variants
from pm4py.algo.conformance.alignments.versions.state_equation_a_star import apply
from pm4py.algo.conformance.alignments.versions.state_equation_a_star import apply_trace_net

from proved.artifacts.behavior_graph import tr_behavior_graph
from proved.artifacts.behavior_net import behavior_net


def alignment_bounds_su_log(log, petri_net, initial_marking, final_marking, parameters=None):
    """
    Returns the lower and upper bounds for conformance of a strongly uncertain log against a reference Petri net.

    :param log: the strongly uncertain event log
    :param petri_net: the reference Petri net
    :param initial_marking: the initial marking of the reference Petri net
    :param final_marking: the final marking of the reference Petri net
    :param parameters: the optional parameters for alignments
    :return: a list of 2-tuples containing the alignment results for the upper and lower bounds for conformance of the traces in the log
    """

    return [alignment_bounds_su_trace(u_trace, petri_net, initial_marking, final_marking, parameters) for u_trace in log]


def alignment_bounds_su_trace(trace, petri_net, initial_marking, final_marking, parameters=None):
    """
    Returns the lower and upper bounds for conformance of a strongly uncertain trace against a reference Petri net by aligning all possible realizations.

    :param trace: the strongly uncertain trace
    :param petri_net: the reference Petri net
    :param initial_marking: the initial marking of the reference Petri net
    :param final_marking: the final marking of the reference Petri net
    :param parameters: the optional parameters for alignments
    :return: a 2-tuple containing the alignment results for the upper and lower bounds for conformance of the trace
    """

    # Obtains the behavior net of the trace
    trace_net = behavior_net.BehaviorNet(tr_behavior_graph.TRBehaviorGraph(trace))

    return (alignment_lower_bound_su_trace(trace_net, trace_net.initial_marking, trace_net.final_marking, petri_net, initial_marking, final_marking, parameters),
            alignment_upper_bound_su_trace_bruteforce(trace_net, trace_net.initial_marking, trace_net.final_marking, petri_net, initial_marking, final_marking, parameters))


def alignment_upper_bound_su_trace_bruteforce(trace_net, tn_i, tn_f, petri_net, initial_marking, final_marking, parameters=None):
    """
    Returns the upper bound for conformance of a strongly uncertain trace against a reference Petri net by aligning all possible realizations.

    :param trace_net: the behavior net of a strongly uncertain trace
    :param petri_net: the reference Petri net
    :param initial_marking: the initial marking of the reference Petri net
    :param final_marking: the final marking of the reference Petri net
    :param parameters: the optional parameters for alignments
    :return: the alignment results for the upper bound for conformance of the trace
    """

    # Obtains all the realizations of the trace by executing all possible variants from the behavior net
    realization_set = acyclic_net_variants(trace_net, tn_i, tn_f)

    # Computes the upper bound for conformance via bruteforce on the realization set
    worst_alignment = None
    for trace in realization_set:
        alignment = apply(trace, petri_net, initial_marking, final_marking, parameters)
        if alignment['cost'] > worst_alignment['cost']:
            worst_alignment = alignment

    return worst_alignment


def alignment_lower_bound_su_trace(trace_net, tn_i, tn_f, petri_net, initial_marking, final_marking, parameters=None):
    """
    Returns the lower bound for conformance of a strongly uncertain trace against a reference Petri net by aligning using the product between the reference Petri net and the behavior net of the trace.

    :param trace_net: the behavior net of a strongly uncertain trace
    :param petri_net: the reference Petri net
    :param initial_marking: the initial marking of the reference Petri net
    :param final_marking: the final marking of the reference Petri net
    :param parameters: the optional parameters for alignments
    :return: the alignment results for the lower bound for conformance of the trace
    """

    return apply_trace_net(petri_net, initial_marking, final_marking, trace_net, tn_i, tn_f, parameters)
