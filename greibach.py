#!/usr/bin/env python

# Trabalho pratico LFA
# Alunos: Samuel Correa e Francisco Abreu

import json
import sys

def contains(str, vector):
    result = False
    for character in vector:
        if str == character:
            result = True
    return result

def has_rule(str, rules):
    result = False
    for rule in rules:
        if rule[1] == str:
            result = True
    return result

def new_rule(expression):
    new_symbol = chr(64+len(symbols)+1)
    new_symbol = str(new_symbol)
    symbols.append(new_symbol)
    new_rule = [new_symbol, expression]
    rules.append(new_rule)
    new_symbol = str(new_symbol)
    return new_symbol

def remover_recursao(symbol, expression):
    new_symbol = chr(64+len(symbols)+1)
    new_symbol = str(new_symbol)
    symbols.append(new_symbol)
    expressao = expression[1:]
    rules.append([new_symbol, expressao])
    rules.append([new_symbol, expressao + new_symbol])
    modified_rules = []
    for i, rule in enumerate(rules):
        symbol_now = rule[0]
        if symbol in symbol_now:
            modified_rules.append([i+1, rule[1]+new_symbol])
    # print(modified_rules)
    for rule in modified_rules:
        # print(rule[1])
        rules.insert(rule[0], [symbol, rule[1]])
        
def troca_simbolo(symbol, expression, index):
    # print(symbol, expression)
    modified_rules = []
    for rule in rules:
        if expression[0] in rule[0]:
            modified_rules.append([index, rule[1]+expression[1:]])
            # print(modified_rules)
    for rule in modified_rules:
        rules.insert(rule[0], [symbol, rule[1]])

def passo_1(final_symbol):
    for rule in rules:
        symbol = rule[0]
        expression = rule[1]
        if symbols.index(symbol) <= symbols.index(final_symbol):
            if len(expression) >= 2:
                for i in range(len(expression)):
                    if i == 0:
                        pass
                    else:
                        if contains(expression[i], alphabet):
                            new_symbol = new_rule(expression[i])
                            rule[1] = expression[:i]+new_symbol+expression[i+1:]

def passo_2(final_symbol):
    for index, rule in enumerate(rules):
        symbol = rule[0]
        expression = rule[1]
        if symbols.index(symbol) <= symbols.index(final_symbol):
            if len(expression) > 1 and contains(expression[0], symbols): 
                if (symbols.index(symbol) >= symbols.index(expression[0])):
                    if symbols.index(symbol) == symbols.index(expression[0]):
                        # print('Recursão a esquerda', symbol, expression)
                        rules.remove(rule)
                        remover_recursao(symbol, expression)
                        passo_2(final_symbol)
                    elif symbols.index(symbol) > symbols.index(expression[0]):
                        # print(
                        #   'Trocar simbolo no inicio da espressão por regras 
                        # deste simbolo concatenado com o resto', symbol, 
                        # expression)
                        rules.remove(rule)
                        troca_simbolo(symbol, expression, index)
                        passo_2(final_symbol)

def passo_3(final_symbol):
    for index in range(len(rules)-1, -1, -1):
        symbol = rules[index][0]
        expression = rules[index][1]
        if symbols.index(symbol) <= symbols.index(final_symbol):
            if len(expression) > 1: 
                if contains(expression[0], symbols):
                    if (symbols.index(symbol) < symbols.index(expression[0])):
                        # print(
                        #     'Trocar simbolo no inicio da espressão por 
                        # regras deste simbolo concatenado com o resto', 
                        # symbol, expression)
                        rules.remove(rules[index])
                        troca_simbolo(symbol, expression, index)

def passo_4(final_symbol):
    for index, rule in enumerate(rules):
        symbol = rule[0]
        expression = rule[1]
        if symbols.index(symbol) >= symbols.index(final_symbol):
            if len(expression) > 1:
                if contains(expression[0], symbols):
                    #  print(
                    #          'Trocar simbolo no inicio da espresão por 
                    # regras deste simbolo concatenado com o resto', symbol, 
                    # expression)
                    rules.remove(rule)
                    troca_simbolo(symbol, expression, index)

try:
    file_name = sys.argv[1]
    f = open(file_name)
    data = json.load(f)
except (IndexError, OSError):
    print(f'Usar: {sys.argv[0]} [GLC]')
else:
    language = data['glc']
    symbols = language[0]
    alphabet = language[1]
    rules = language[2]
    final_symbol = symbols[len(symbols)-1]
    # passo 1
    passo_1(final_symbol)
    # passo 2
    passo_2(final_symbol)
    # passo 3
    passo_3(final_symbol)  
    # passo 4
    passo_4(final_symbol)
    rules.sort()

    saida = {
        "glc":[symbols, alphabet, rules, language[3]]
    }
    print(saida)
    outfile = open("saida.json", "w")
    json.dump(saida, outfile)