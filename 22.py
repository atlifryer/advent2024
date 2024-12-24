from collections import defaultdict
import sys


def mix_and_prune(secret, value):
    secret ^= value
    secret %= 16777216
    return secret


def generate_next_secret(secret):
    secret = mix_and_prune(secret, secret * 64)
    secret = mix_and_prune(secret, secret // 32)
    secret = mix_and_prune(secret, secret * 2048)
    return secret


def simulate_buyer(initial_secret, steps):
    secret = initial_secret
    for _ in range(steps):
        secret = generate_next_secret(secret)
    return secret


def simulate_prices(initial_secret, steps):
    secret = initial_secret
    prices = []
    for _ in range(steps):
        secret = generate_next_secret(secret)
        prices.append(secret % 10)
    changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    return prices, changes


def find_best_sequence_efficient(initial_secrets, steps):
    all_prices = []
    all_changes = []
    for secret in initial_secrets:
        prices, changes = simulate_prices(secret, steps)
        all_prices.append(prices)
        all_changes.append(changes)

    sequence_scores = defaultdict(int)

    for prices, changes in zip(all_prices, all_changes):
        seen_sequence = set()
        for i in range(len(changes) - 3):
            sequence = tuple(changes[i : i + 4])
            if sequence in seen_sequence:
                continue
            if i + 4 < len(prices):
                sequence_scores[sequence] += prices[i + 4]
                seen_sequence.add(sequence)

    best_sequence = max(sequence_scores, key=sequence_scores.get)
    max_bananas = sequence_scores[best_sequence]

    return best_sequence, max_bananas


initial_secrets = [int(x) for x in sys.stdin.read().strip().split("\n")]
steps = 2000

# Part 1
total = sum(simulate_buyer(secret, steps) for secret in initial_secrets)
print(f"Part 1: {total}")

# Part 2
best_sequence, max_bananas = find_best_sequence_efficient(initial_secrets, steps)
print(f"Part 2: {best_sequence} results in {max_bananas} bananas")
