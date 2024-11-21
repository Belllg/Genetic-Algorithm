# UNIBRASIL Maps - Projeto de Planejamento de Roteiro de Deslocamento de Drone

## Descrição

O projeto **UNIBRASIL Maps** tem como objetivo planejar o roteiro de deslocamento de um drone autônomo para mapear a cidade de Curitiba. O drone deve visitar uma lista de CEPs fornecida, coletando imagens em cada localização e retornando ao ponto inicial (Campus Unibrasil) de forma otimizada. O objetivo é minimizar o custo, que será medido pelo tempo total de voo e pela quantidade de paradas para recarga.

Este projeto foi desenvolvido como parte da **Atividade Discente Supervisionada 2** da disciplina de **Serviços Cognitivos**, sob a supervisão do **Prof. Mozart Hasse**.

### Requisitos do Projeto

- O algoritmo utilizado para a otimização do percurso será baseado em **computação evolucionária**, especificamente um **algoritmo genético**.
- O drone possui uma velocidade base de 30 km/h e uma velocidade máxima de 60 km/h, sendo a velocidade real influenciada pelo efeito do vento.
- O tempo de voo entre as coordenadas é calculado em segundos, e a autonomia do drone é de 30 minutos, considerando as paradas para fotografia e recarga.
- A solução deve ser gerada em um arquivo CSV contendo as informações sobre os voos, incluindo CEPs de partida e chegada, horários de decolagem e chegada, velocidade, entre outros.


### Detalhes Técnicos
Cálculo de Distâncias: A distância entre coordenadas foi calculada utilizando a fórmula Haversine, conforme orientação.
Consumo de Energia: O consumo de energia foi ajustado com base na velocidade de voo do drone e na direção/velocidade do vento. Para cada voo, foi calculada a redução da autonomia.
Cálculo do Tempo de Voo: O tempo de voo entre as coordenadas foi calculado levando em consideração a velocidade real do drone, a distância a ser percorrida e o efeito do vento.
Estrutura do Arquivo CSV de Saída
O arquivo output.csv gerado contém as seguintes colunas:

CEP inicial: Código do CEP de onde o voo começa.
Latitude inicial: Latitude da coordenada inicial.
Longitude inicial: Longitude da coordenada inicial.
Hora inicial: Hora de decolagem do drone.
Velocidade: Velocidade de voo (em km/h) considerando o ajuste do vento.
CEP final: Código do CEP de destino.
Latitude final: Latitude da coordenada de destino.
Longitude final: Longitude da coordenada de destino.
Pouso: Indica se o drone pousou ou não na coordenada (SIM ou NÃO).
Hora final: Hora de chegada à coordenada de destino.

### Cuidados na Implementação
A implementação deve garantir que o drone nunca fique sem carga durante o voo.
A solução deve ser otimizada quanto ao tempo total de voo e à quantidade de paradas para recarga.
O código deve ser bem estruturado, com uma função fitness clara e eficiente para avaliar as soluções geradas pelo algoritmo genético.
Devem ser realizados testes unitários para garantir a precisão dos cálculos de distância, tempo de voo, e consumo de energia.
Equipe

### Este projeto foi desenvolvido por:

Giovani Bellani - 2022100204
Gustavo Henrique Tureck RA:2022101462
Beatriz Marques - 2019101867
