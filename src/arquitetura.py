from functools import partial  # noqa: INP001

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom

# ============================================================================ #
# Digital Ocean resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/digitalocean
#
from diagrams.digitalocean.network import LoadBalancer

# ============================================================================ #
# Kubernetes resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/k8s
#
# ============================================================================ #
# On-premise / Open Source resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/onprem
#
from diagrams.onprem.client import Users
from diagrams.onprem.network import Kong, Nginx
from diagrams.onprem.queue import Kafka

# ============================================================================ #
# Programming resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/programming
#
from diagrams.programming.framework import React, Vue
from diagrams.programming.language import Go, NodeJS, Python

# ============================================================================ #
# SaaS:
#
#   https://diagrams.mingrammer.com/docs/nodes/saas
#
from diagrams.saas.cdn import Cloudflare
from diagrams.saas.chat import Discord, Telegram

# ============================================================================ #

# https://www.graphviz.org/doc/info/attrs.html
graph_attr = {
    "rankdir": "TB",
    "nodesep": "1",
    "ranksep": "1.5",
    "pad": "0.5",
    "fontsize": "28",
    "labeljust": "c",
    "labelloc": "t",
    "label": "Arquitetura Lifeapps",
    "compound": "true",
    "center": "true",
}

edge_attr = {
    "fontsize": "20",
    "arrowhead": "vee",
    "penwidth": "4",
}

Rest = partial(Edge, color="dodgerblue")
Grpc = partial(Edge, style="dashed", color="firebrick")
GraphQL = partial(Edge, style="dashed", color="pink")
Stream = partial(Edge, style="dashed", color="orange")
Socket = partial(Edge, style="dashed", color="slateblue")
Webhook = partial(Edge, style="dashed", color="mediumseagreen")

# pylint: disable=W0104,W0106
with Diagram(
    "Arquitetura Lifeapps",
    show=False,
    direction="TB",
    filename="result/arquitetura_lifeapps",
    graph_attr=graph_attr,
    edge_attr=edge_attr,
):
    users = Users("Internet Users")

    with Cluster("Cloudflare"):
        dns = Cloudflare("Cloudflare\nDNS")
        (
            users
            >> Edge(
                lhead="cluster_Cloudflare",
            )
            >> dns
        )

    with Cluster("Digital Ocean"):
        load_balancer = LoadBalancer("K8S Load Balancer")
        dns >> Rest() >> load_balancer

        with Cluster("Kubernetes Cluster"):
            with Cluster("Ingress"):
                nginx = Nginx("Nginx\nIngress Controller")
                (
                    load_balancer
                    >> Rest(
                        lhead="cluster_Ingress",
                    )
                    >> nginx
                )
            with Cluster("Web Applications"):
                webcommerce = React("WebCommerce")
                backoffice = Vue("Backoffice")
                menu_unico = Vue("Menu Único")
                faturamento = Vue("Faturamento")
                paje = Vue("Pajé")
                botinho = React("Botinho")
                cashback = React("Cashback")
                (
                    nginx
                    >> Rest(
                        ltail="cluster_Ingress",
                        lhead="cluster_Web Applications",
                        minlen="2",
                    )
                    >> [
                        webcommerce,
                        botinho,
                        cashback,
                        backoffice,
                        menu_unico,
                        paje,
                        faturamento,
                    ]
                )

            with Cluster("Api Gateway"):
                kong = Kong("Kong")
                (
                    [
                        webcommerce,
                        botinho,
                        cashback,
                        backoffice,
                        menu_unico,
                        paje,
                        faturamento,
                    ]
                    >> Rest(
                        ltail="cluster_Web Applications",
                        lhead="cluster_Api Gateway",
                        minlen="2",
                    )
                    >> kong
                )
            with Cluster("Microservices", direction="LR"):
                with Cluster("Saas"):
                    rd_station = Custom("RD Station", "../icons/rd_station.png")
                    one_signal = Custom("OneSignal", "../icons/onesignal.png")
                    zenvia = Custom("Zenvia", "../icons/zenvia.png")
                    blip = Custom("Blip", "../icons/blip.png")
                    elastic_email = Custom(
                        "Elastic Email", "../icons/elastic_email.png"
                    )
                    telegram = Telegram("Telegram")
                    discord = Discord("Discord")
                with Cluster("E-commerce"):
                    server = NodeJS("Superon Server")
                    payment = NodeJS("Payment")
                    frete = NodeJS("Frete")
                    spreadsheet = NodeJS("Spreadsheet")
                    order = NodeJS("Order")
                    telebot = NodeJS("Telebot")
                    indexed_search = NodeJS("Indexed Search")
                    image_proxy = Go("Image Proxy")
                    irecommend = Python("IRecommend")
                    chateado = NodeJS("Chateado")
                    authenticator = NodeJS("Authenticator")
                    dadospublicos = NodeJS("Dados Públicos")
                    message_job = Python("Message Job")
                    prupru = NodeJS("Prupru")
                    rdstation_notifier = NodeJS("RDStation Notifier")
                    message_notifier = NodeJS("Message Notifier")
                    pizzaroll = NodeJS("Pizzaroll")
                    webcommerce - Socket() - chateado
                    message_notifier >> Rest() >> [one_signal, blip, zenvia]
                    rdstation_notifier >> Rest() >> rd_station
                    telebot >> Rest() >> telegram
                    message_job >> Rest() >> elastic_email
                    server >> Webhook() >> discord
                with Cluster("Botinho"):
                    api_atendimento = NodeJS("API Atendimento")
                    api_socket = NodeJS("API Socket")
                    botinho - Socket() - api_socket
                with Cluster("Integração"):
                    paje = Go("Pajé")
                with Cluster("Menu Único"):
                    menu_unico_api = NodeJS("Menu Único API")
                    faturamento = NodeJS("Faturamento")
                (
                    kong
                    >> Rest(
                        ltail="cluster_Api Gateway",
                        minlen="2",
                    )
                    >> [
                        server,
                        payment,
                        frete,
                        spreadsheet,
                        order,
                        indexed_search,
                        irecommend,
                        paje,
                        faturamento,
                        authenticator,
                        dadospublicos,
                        prupru,
                        image_proxy,
                        menu_unico_api,
                        api_atendimento,
                    ]
                )
                (server >> Grpc(label="Consulta Preço") >> paje)
                (paje >> Rest() >> server)
            with Cluster("Message Broker"):
                kafka = Kafka("Kafka Cluster")
                (
                    [
                        server,
                        payment,
                        spreadsheet,
                        order,
                        irecommend,
                        chateado,
                        faturamento,
                        prupru,
                        image_proxy,
                        api_atendimento,
                        api_socket,
                    ]
                    >> Stream(
                        lhead="cluster_Message Broker",
                        minlen="2",
                    )
                    >> kafka
                )
