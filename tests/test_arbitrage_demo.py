"""Unit tests for the Forex Currency Arbitrage demonstration."""
from __future__ import annotations
import math
import pytest
from graph.demo.currency_arbitrage_demo import (
    build_forex_graph,
    find_arbitrage_cycle,
    run_currency_arbitrage_demo,
    DEFAULT_EXCHANGE_RATES,
)


def test_build_forex_graph():
    graph, nodes = build_forex_graph(DEFAULT_EXCHANGE_RATES)
    assert len(nodes) == 6
    assert "USD" in nodes
    assert "EUR" in nodes
    assert "JPY" in nodes

    # Check transformed log weight for USD -> EUR
    usd_node = nodes["USD"]
    eur_edge = [e for e in usd_node.edges if e.t.name == "EUR"][0]
    expected_weight = -math.log(DEFAULT_EXCHANGE_RATES[("USD", "EUR")])
    assert pytest.approx(eur_edge.weight, abs=1e-5) == expected_weight


def test_find_arbitrage_cycle():
    graph, nodes = build_forex_graph(DEFAULT_EXCHANGE_RATES)
    cycle = find_arbitrage_cycle(graph, DEFAULT_EXCHANGE_RATES, start_code="USD")
    assert cycle is not None
    assert len(cycle) >= 3
    assert cycle[0] == cycle[-1]  # Must be a valid cycle


def test_run_currency_arbitrage_demo(capsys):
    run_currency_arbitrage_demo()
    captured = capsys.readouterr()
    assert "REAL-WORLD DEMO: Forex Currency Arbitrage Detection" in captured.out
    assert "ARBITRAGE OPPORTUNITY DETECTED" in captured.out
    assert "Trade Simulation" in captured.out
    assert "Net Profit" in captured.out
