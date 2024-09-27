from .impls.depth_exp import ExponentialDepthAutomaton
from .impls.lazy_top_3 import LazyTop3Automaton


ALL_AUTOMATAS = {
    "exponential_depth": ExponentialDepthAutomaton,
    "lazy_top_3": LazyTop3Automaton,
}
