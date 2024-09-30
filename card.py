import copy
from dataclasses import dataclass

from settings import LLM_API


@dataclass
class Card:
    concept: str
    name: str = ""
    mana_cost: str = ""
    card_type: str = ""
    text: str = ""
    flavor_text: str = ""
    power_and_toughness: str = ""

    def __str__(self) -> str:
        return (
            f"CONCEPT:\n{self.concept}\n\n"
            f"NAME: {self.name or "(Not decided yet)"}\n"
            f"MANA COST: {self.mana_cost or "(Not decided yet)"}\n"
            f"CARD TYPE: {self.card_type or "(Not decided yet)"}\n"
            f"TEXT: {self.text or "(Not decided yet)"}\n"
            f"FLAVOR TEXT: {self.flavor_text or "(Not decided yet)"}\n"
            f"POWER AND TOUGHNESS: {self.power_and_toughness or "(Not decided yet)"}\n"
        )

    @property
    def basic_info(self) -> str:
        """Card info without the concept"""
        return (
            f"NAME: {self.name or "(Not decided yet)"}\n"
            f"MANA COST: {self.mana_cost or "(Not decided yet)"}\n"
            f"CARD TYPE: {self.card_type or "(Not decided yet)"}\n"
            f"TEXT: {self.text or "(Not decided yet)"}\n"
            f"FLAVOR TEXT: {self.flavor_text or "(Not decided yet)"}\n"
            f"POWER AND TOUGHNESS: {self.power_and_toughness or "(Not decided yet)"}\n"
        )

    def copy_and_update(self, **kwargs) -> "Card":
        self_copy = copy.deepcopy(self)

        for key, value in kwargs.items():
            if hasattr(self_copy, key):
                setattr(self_copy, key, value)
            else:
                raise AttributeError(
                    f"{self.__class__.__name__} has no attribute '{key}'"
                )

        return self_copy


def generate_concept() -> Card:
    concept = LLM_API.response_from_prompt(
        "Please create a basic concept for a Magic the Gathering card. No need for specifics yet, keep it high level. Theme, color(s), card type, possible lore, etc."
    )
    return Card(concept=concept)


def generate_name(card: Card) -> Card:
    prompt = (
        f"Please give me a name for a Magic the Gathering card. Here's the current concept for the card:\n"
        f"\n"
        f"{str(card)}\n"
        f"\n"
        f"Respond with the name only. No quotation marks needed."
    )
    name = LLM_API.response_from_prompt(prompt)
    return card.copy_and_update(name=name)


def generate_mana_cost(card: Card) -> Card:
    prompt = f"""Please give me a mana cost for a Magic the Gathering card. Here's the current concept for the card:

{str(card)}

Use the common abbreviations for different kinds of mana:
  - W for white
  - U for blue
  - B for black
  - R for red
  - G for green
  - just a number for colorless
  
Respond with the mana cost for the card only.
 """
    mana_cost = LLM_API.response_from_prompt(prompt)
    return card.copy_and_update(mana_cost=mana_cost)


def generate_card_type(card: Card) -> Card:
    prompt = f"""Please give me card type(s) for a Magic the Gathering card. Here's the current concept for the card:

{str(card)}

Card types include: artifact, creature, enchantment, instant, land, planeswalker, tribal, sorcery
Include possible super- and subtypes.
  
Respond with the card type only.
 """
    card_type = LLM_API.response_from_prompt(prompt)
    return card.copy_and_update(card_type=card_type)


def generate_text(card: Card) -> Card:
    prompt = f"""Please give me the text (the rules text, not the flavour text) for a Magic the Gathering card. Here's the current concept for the card:

{str(card)}
  
Respond with the rules text (that's going to be inside the text box of the card) only.
 """
    card_text = LLM_API.response_from_prompt(prompt)
    return card.copy_and_update(text=card_text)


def generate_flavor_text(card: Card) -> Card:
    prompt = f"""Please give me the flavor text for a Magic the Gathering card. Here's the current concept for the card:

{str(card)}
  
Respond with the flavor text only.
 """
    flavor_text = LLM_API.response_from_prompt(prompt)
    return card.copy_and_update(flavor_text=flavor_text)


def generate_power_toughness(card: Card) -> Card:
    prompt = f"""Please give me the power and toughness for a Magic the Gathering card, if applicable. Here's the current concept for the card:

{str(card)}
  
Respond either with the power and toughness in the form of "6 / 5" or "(not applicable)". Don't include the quotes in your response.
 """
    power_and_toughness = LLM_API.response_from_prompt(prompt)
    return card.copy_and_update(power_and_toughness=power_and_toughness)


def generate_card() -> Card:
    crd: Card = generate_concept()
    crd = generate_name(crd)
    crd = generate_mana_cost(crd)
    crd = generate_card_type(crd)
    crd = generate_text(crd)
    crd = generate_power_toughness(crd)
    crd = generate_flavor_text(crd)
    return crd
