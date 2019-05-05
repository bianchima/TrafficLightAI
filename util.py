from enum import Enum

class Card(Enum):
    # Cardinal direction the cars are traveling towards
    S = "South"
    E = "East"
    N = "North"
    W = "West"

intersection_states = [
  ((Card.E, Card.N), (Card.S, Card.W), (Card.N, Card.E), (Card.W, Card.S)),
  ((Card.E, Card.N), (Card.S, Card.W), (Card.N, Card.E), (Card.E, Card.S)),
  ((Card.E, Card.N), (Card.S, Card.W), (Card.E, Card.E), (Card.E, Card.S)),
  ((Card.N, Card.N), (Card.S, Card.S), (Card.S, Card.W), (Card.N, Card.E)),
  ((Card.N, Card.N), (Card.S, Card.W), (Card.N, Card.E), (Card.E, Card.S)),
  ((Card.N, Card.N), (Card.N, Card.E), (Card.E, Card.S), (Card.N, Card.W)),
  ((Card.S, Card.S), (Card.W, Card.N), (Card.S, Card.W), (Card.N, Card.E)),
  ((Card.S, Card.S), (Card.W, Card.N), (Card.S, Card.W), (Card.S, Card.E)),
  ((Card.W, Card.N), (Card.S, Card.W), (Card.N, Card.E), (Card.W, Card.S)),
  ((Card.W, Card.N), (Card.S, Card.W), (Card.N, Card.E), (Card.E, Card.S)),
  ((Card.W, Card.N), (Card.S, Card.W), (Card.E, Card.E), (Card.E, Card.S)),
  ((Card.W, Card.N), (Card.S, Card.W), (Card.E, Card.S), (Card.S, Card.E)),
  ((Card.W, Card.N), (Card.N, Card.E), (Card.W, Card.W), (Card.W, Card.S)),
  ((Card.W, Card.N), (Card.N, Card.E), (Card.W, Card.W), (Card.E, Card.S)),
  ((Card.W, Card.N), (Card.N, Card.E), (Card.E, Card.S), (Card.N, Card.W)),
  ((Card.W, Card.N), (Card.W, Card.W), (Card.E, Card.E), (Card.E, Card.S)),
  ((Card.W, Card.N), (Card.E, Card.S), (Card.S, Card.E), (Card.N, Card.W))
]

DIRECTION_COLORS = {
    Card.N : "salmon",
    Card.S : "red",
    Card.E : "blue",
    Card.W : "cyan",
}
