#!/usr/bin/env python3
# Student: [Tomasz Giedrojc]
# Student ID: [100793058]
# TPRG2131 - Project 1: Vending Machine

import PySimpleGUI as sg

# Vending Machine class with state machine
class VendingMachine:
    """Vending Machine state machine class to manage coins, products, and change."""
    PRODUCTS = {
        "Cheetos": ("Cheetos", 300),   # Price in cents
        "Kitkat": ("Kitkat", 135),
        "Pepsi": ("Pepsi", 325),
        "Sourpatch Kids": ("Sourpatch Kids", 135),
        "Sprite": ("Sprite", 325)
    }
    COINS = {
        "5": ("5¢", 5),
        "10": ("10¢", 10),
        "25": ("25¢", 25),
        "100": ("$1", 100),
        "200": ("$2", 200)
    }

    def __init__(self):
        """Initializes the vending machine with default values."""
        self.state = None
        self.states = {}
        self.event = ""
        self.amount = 0
        self.change_due = 0
        values = [self.COINS[k][1] for k in self.COINS]
        self.coin_values = sorted(values, reverse=True)

    def add_state(self, state):
        """Adds a new state to the vending machine state machine."""
        self.states[state.name] = state

    def go_to_state(self, state_name):
        """Transitions the vending machine to a new state."""
        if self.state:
            self.state.on_exit(self)
        self.state = self.states[state_name]
        self.state.on_entry(self)

    def update(self):
        """Updates the current state of the vending machine."""
        if self.state:
            self.state.update(self)

    def add_coin(self, coin):
        """Adds the value of a coin to the total inserted amount."""
        self.amount += self.COINS[coin][1]

    def calculate_change(self):
        """Calculates and returns the coins needed for the change."""
        change = []
        for coin in self.coin_values:
            while self.change_due >= coin:
                change.append(coin)
                self.change_due -= coin
        return change

# Abstract state class
class State:
    """Abstract superclass for vending machine states."""
    _NAME = ""
    def __init__(self):
        pass

    @property
    def name(self):
        return self._NAME

    def on_entry(self, machine):
        """Actions when entering a state."""
        pass

    def on_exit(self, machine):
        """Actions when exiting a state."""
        pass

    def update(self, machine):
        """State update logic, to be implemented by concrete states."""
        pass

class WaitingState(State):
    _NAME = "waiting"

    def update(self, machine):
        """Update logic when in the 'waiting' state."""
        if machine.event in machine.COINS:
            machine.add_coin(machine.event)
            machine.go_to_state('add_coins')

class AddCoinsState(State):
    _NAME = "add_coins"

    def update(self, machine):
        """Update logic for the 'add_coins' state."""
        if machine.event == "RETURN":
            # Calculate change due and reset the amount to 0
            machine.change_due = machine.amount
            machine.amount = 0
            machine.go_to_state('count_change')
        elif machine.event in machine.COINS:
            machine.add_coin(machine.event)
        elif machine.event in machine.PRODUCTS:
            price = machine.PRODUCTS[machine.event][1]
            if machine.amount >= price:
                machine.change_due = machine.amount - price
                machine.amount = 0
                machine.go_to_state('count_change')

class CountChangeState(State):
    _NAME = "count_change"

    def on_entry(self, machine):
        """On entry to 'count_change', calculate the change to return."""
        change = machine.calculate_change()
        if change:
            print(f"Returning change: {', '.join([f'{c}¢' for c in change])}")
        else:
            print("No change to return.")
        machine.go_to_state('waiting')

# PySimpleGUI setup
sg.theme('BluePurple')

# Build the coin buttons
coin_col = [[sg.Text("ENTER COINS", font=("Helvetica", 24))]]
for item in VendingMachine.COINS:
    button = sg.Button(item, font=("Helvetica", 18))
    coin_col.append([button])

# Build the product selection buttons and display their prices
select_col = [[sg.Text("SELECT ITEM", font=("Helvetica", 24))]]
for item in VendingMachine.PRODUCTS:
    price = VendingMachine.PRODUCTS[item][1] / 100  # Price in dollars
    button = sg.Button(f"{item} - ${price:.2f}", font=("Helvetica", 18))
    select_col.append([button])

# Layout for the window
layout = [
    [sg.Column(coin_col, vertical_alignment="TOP"),
     sg.VSeparator(),
     sg.Column(select_col, vertical_alignment="TOP")],
    [sg.Text("Amount Inserted: $0.00", key="AMOUNT", font=("Helvetica", 16)),
     sg.Text("Change Due: $0.00", key="CHANGE", font=("Helvetica", 16)),
     sg.Text("Current State: waiting", key="STATE", font=("Helvetica", 16))],
    [sg.Button("RETURN", font=("Helvetica", 12))],
]

window = sg.Window('Vending Machine', layout, finalize=True)

# Initialize the VendingMachine instance and states
vending = VendingMachine()
vending.add_state(WaitingState())
vending.add_state(AddCoinsState())
vending.add_state(CountChangeState())
vending.go_to_state('waiting')

# Main Event Loop
while True:
    event, values = window.read(timeout=10)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    # Handle GUI button presses
    if event in vending.COINS:
        vending.event = event
        vending.update()
    elif event in vending.PRODUCTS:
        vending.event = event
        vending.update()
    elif event == "RETURN":
        vending.event = event
        vending.update()

    # Update GUI based on current state
    window["AMOUNT"].update(f"Amount Inserted: ${vending.amount / 100:.2f}")
    window["CHANGE"].update(f"Change Due: ${vending.change_due / 100:.2f}")
    window["STATE"].update(f"Current State: {vending.state.name}")

window.close()
print("Normal exit")
