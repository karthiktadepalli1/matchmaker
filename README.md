# Readme

`matchmaker` is a codebase in progress on which researchers can build to run simulations of matching markets, assignment markets, and dynamic matching markets. It implements markets as undirected graphs and produces matchings as undirected graphs with edges between two matched nodes. `matchmaker` is built upon the `networkx` library.

### Goals

Matching simulations are useful in two main contexts:
1. A researcher has a dataset of preferences for market participants, and wants to analyze counterfactual markets with this data. This frequently uses canonical mechanisms as comparisons, and quick-access implementations of those mechanisms would be helpful.
2. A researcher wants to analyze a complex, multi-parameter market. The number of free parameters (e.g. time, entry/exit, compatibility, non-convex preferences, etc) makes this less amenable to theoretical analysis, so they would like to run simulations to see the outcomes of such a market.

The goal, then, is to aid researchers in both of these contexts. Three design features will help accomplish this:
1. **Comprehensiveness** - the goal is to implement the most commonly-used subset of matching algorithms, making lives easier for the researchers who would otherwise have to implement these algorithms themselves.
2. **Usability** - researchers are not the most tech-savvy people, and user-friendliness makes it more likely that they will prefer this package. Providing the tools very simply and making it easy to produce good visualizations is essential here.
3. **Flexibility** - most researchers are working on matching models at the cutting edge, which means we necessarily cannot build those models in. The goal is to allow researchers to fork our code to implement their models relatively easily.

### TODOs (9/30/20)

1. Modify the setup to implement:
 - dynamic matching
 - many-to-one matching
2. New algorithms:
 - competitive equilibrium with equal incomes
3. Introduce visualization tools built on networkx and nxviz.
4. Modify the implemented algorithms to work with indifferences in preferences.
5. Introduce richer type spaces/utility functions rather than relying solely on ranks.
