# UNIBRASIL Maps - Projeto de Planejamento de Roteiro de Deslocamento de Drone

## Descrição

O projeto **UNIBRASIL Maps** tem como objetivo planejar o roteiro de deslocamento de um drone autônomo para mapear a cidade de Curitiba. O drone deve visitar uma lista de CEPs fornecida, coletando imagens em cada localização e retornando ao ponto inicial (Campus Unibrasil) de forma otimizada. O objetivo é minimizar o custo, que será medido pelo tempo total de voo e pela quantidade de paradas para recarga.

Este projeto foi desenvolvido como parte da **Atividade Discente Supervisionada 2** da disciplina de **Serviços Cognitivos**, sob a supervisão do **Prof. Mozart Hasse**.

### Requisitos do Projeto

- O algoritmo utilizado para a otimização do percurso será baseado em **computação evolucionária**, especificamente um **algoritmo genético**.
- O drone possui uma velocidade base de 30 km/h e uma velocidade máxima de 60 km/h, sendo a velocidade real influenciada pelo efeito do vento.
- O tempo de voo entre as coordenadas é calculado em segundos, e a autonomia do drone é de 30 minutos, considerando as paradas para fotografia e recarga.
- A solução deve ser gerada em um arquivo CSV contendo as informações sobre os voos, incluindo CEPs de partida e chegada, horários de decolagem e chegada, velocidade, entre outros.

