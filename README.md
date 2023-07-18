# TCC

## Main

Ambos 'Main.py' e 'Main.ipynb' servem a mesma função, que é a de executar as instâncias utilizando-se do GUROBIPY.
A principal diferença é que o notebook apresenta uma breve explicação das funções implementadas no algoritmo.

## buildtable.py

Monta as tabelas detalhadas de cada bateria de testes, apresentando informações de instância executada

## buildstatistics.py

Cria as tabelas que apresentam informações referentes a grupos de instâncias de cada bateria de testes

## Instances/

Onde estão armazenadas todas as 320 instâncias utilizadas nos testes

## Tables/

Pasta contendo as tabelas com as informações referentes aos testes feitos

## tests_0xx_0yy/

Nessas pastas estão contidos tanto os .json obtidos após a execução dos testes, quanto as imagens referentes aos grafos antes e após o distritamento

*xx* representa o valor da tolerância da disparidade das demandas em porcentagem

*yy* representa o valor da tolerância da perda de paridade dos vértices em porcentagem
