
#!/usr/bin/env python3
# Student: [Tomasz Giedrojc]
# Student ID: [100793058]
# TPRG2131 - Project 1: Vending Machine

import pytest
from vending_machine_graphical import VendingMachine, WaitingState, AddCoinsState, CountChangeState

@pytest.fixture
def machine():
    """Fixture to create a VendingMachine instance for testing."""
    machine = VendingMachine()
    machine.add_state(WaitingState())
    machine.add_state(AddCoinsState())
    machine.add_state(CountChangeState())
    machine.go_to_state('waiting')
    return machine

def test_add_coin_5(machine):
    """Test adding a 5¢ coin to the machine."""
    machine.add_coin("5")  # 5¢ coin
    assert machine.amount == 5, f"Expected 5¢, but got {machine.amount}¢"

def test_add_coin_10(machine):
    """Test adding a 10¢ coin to the machine."""
    machine.add_coin("10")  # 10¢ coin
    assert machine.amount == 10, f"Expected 10¢, but got {machine.amount}¢"

def test_add_coin_25(machine):
    """Test adding a 25¢ coin to the machine."""
    machine.add_coin("25")  # 25¢ coin
    assert machine.amount == 25, f"Expected 25¢, but got {machine.amount}¢"

def test_add_coin_100(machine):
    """Test adding a $1 coin (100¢) to the machine."""
    machine.add_coin("100")  # $1 coin
    assert machine.amount == 100, f"Expected 100¢, but got {machine.amount}¢"

def test_add_coin_200(machine):
    """Test adding a $2 coin (200¢) to the machine."""
    machine.add_coin("200")  # $2 coin
    assert machine.amount == 200, f"Expected 200¢, but got {machine.amount}¢"

def test_multiple_coin_addition(machine):
    """Test adding multiple coins and verifying the total amount."""
    machine.add_coin("100")  # $1 coin
    machine.add_coin("25")   # 25¢ coin
    machine.add_coin("10")   # 10¢ coin
    machine.add_coin("5")    # 5¢ coin
    assert machine.amount == 140, f"Expected 140¢, but got {machine.amount}¢"

def test_product_purchase(machine):
    """Test purchasing a product and verifying the amount and state."""
    machine.add_coin("100")  # $1 coin
    machine.add_coin("25")   # 25¢ coin
    machine.event = "Pepsi"
    machine.update()  # Simulate purchasing the product
    assert machine.amount == 0, f"Expected 0¢ after purchase, but got {machine.amount}¢"
    assert machine.change_due == 0, f"Expected 0¢ change due, but got {machine.change_due}¢"

def test_calculate_change(machine):
    """Test that the correct change is calculated after a product is purchased."""
    machine.add_coin("200")  # $2 coin
    machine.event = "Pepsi"
    machine.update()  # Attempt to purchase Pepsi
    assert machine.change_due == 175, f"Expected 175¢ change due, but got {machine.change_due}¢"
    change = machine.calculate_change()
    assert change == [100, 25, 25, 25], f"Expected change to be [100, 25, 25, 25], but got {change}"

