from setuptools import setup, find_namespace_packages

setup(
    name='tradingagents',
    version='0.1.0',
    # We map the "tradingagents" package to the current directory "."
    package_dir={'tradingagents': '.'},
    # We manually list the subpackages since they are in the root directory
    packages=[
        'tradingagents',
        'tradingagents.agents',
        'tradingagents.agents.analysts',
        'tradingagents.agents.managers',
        'tradingagents.agents.researchers',
        'tradingagents.agents.risk_mgmt',
        'tradingagents.agents.trader',
        'tradingagents.agents.utils',
        'tradingagents.dataflows',
        'tradingagents.graph',
        'tradingagents.llm_clients',
    ],
)
