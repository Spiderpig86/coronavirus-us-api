# Makefile for coronavirus-us-api
# Runs combined tasks for CI build

PYTHON ?= python3

API = api

format:
	invoke format

clean-code:
	invoke check --format --sort