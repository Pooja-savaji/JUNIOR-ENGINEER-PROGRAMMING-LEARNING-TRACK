# Bug Notes

## Problem
The discount value could be greater than 100%.

## Fix
Added validation to reject discounts above 100%.

## Regression Test
Added a test to make sure the same bug does not happen again.
