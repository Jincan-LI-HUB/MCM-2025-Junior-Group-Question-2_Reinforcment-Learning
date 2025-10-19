# MCM Game AI - Question (2) Answer

## Experimental Summary
- Alice's win rate: 71.5%
- Top winning openings: [(78, 24241), (72, 1107), (90, 580)]
- Key frequent numbers: [1, 90, 10, 2, 72, 96]

## Final Answer
# Optimal Strategy for Alice in the 1-100 Number Chain Game

## Mathematical Structure

The game can be modeled as a directed graph where each node represents a number from 1 to 100, and an edge from node \(a\) to node \(b\) exists if \(b = k \times a\) and \(b \leq 100\). This structure reveals a hierarchical relationship between numbers, with each node potentially leading to multiple nodes, depending on its factors. Notably, playing a large prime number (\(p > 50\)) forces Bob to play 1, as there are no other numbers \(k \times p\) within the 1-100 range, except for \(p\) itself. This is because primes greater than 50 have no divisors other than 1 and themselves, making them pivotal in controlling the game's flow.

### Core Principle: Controlling the Game Flow

Controlling the game flow by strategically choosing numbers that maximize the number of subsequent moves is crucial. Numbers with a high number of divisors, such as 64 (which is \(2^6\)), enable the longest chains, facilitating a more extended interaction with Bob. This strategy leverages the dense connectivity of numbers that are powers of small primes, allowing Alice to maintain control over the game's progression.

## Critique the Data

While 100 appears frequently in winning games, this observation might not reflect the optimal strategy. The prevalence of 100 could be attributed to a short-term reward bias in the training process, where players might be incentivized to maximize immediate gains over long-term strategic advantages. This could lead to a local optimum, where the strategy of opening with 100 is favored due to its high payoff in the immediate game state, rather than its effectiveness in controlling the game's overall flow.

## Optimal Strategy

### Opening

Alice's optimal opening move should aim to control the game's flow by selecting a number that maximizes the number of subsequent possible moves. A prime number greater than 50 is ideal, as it forces Bob to play 1, thereby setting a foundation for Alice to maintain control over the game's progression. Alternatively, choosing a number that is a power of a small prime (like 64) can also be effective, as it enables a longer chain of moves, potentially leading to a more advantageous position.

### Mid-game

During the mid-game, Alice should focus on controlling key nodes that offer the most potential for subsequent moves. This involves selecting numbers that are either prime or have a high number of divisors, thereby maximizing the number of options available for subsequent turns. By doing so, Alice can strategically manipulate the game's flow, forcing Bob into less favorable positions.

### End-game

In the end-game, the strategy should shift towards securing the final move, which is typically playing 1. Alice should aim to leave Bob with a limited number of options, ideally forcing him to play 1, thus securing the win. This requires careful management of the remaining numbers, ensuring that Bob is left with no viable moves that would allow him to avoid playing 1.

### Core Principle: **Strategic Control over Game Flow**

The optimal strategy for Alice in the 1-100 number chain game hinges on strategic control over the game flow. By selecting numbers that maximize the number of subsequent moves, Alice can maintain a dominant position, forcing Bob into less favorable scenarios and ultimately securing the win.