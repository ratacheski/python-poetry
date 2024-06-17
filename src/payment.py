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
# SaaS:
#
#   https://diagrams.mingrammer.com/docs/nodes/elastic
#
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
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Kong, Nginx
from diagrams.onprem.queue import Kafka

# ============================================================================ #
# Programming resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/programming
#
from diagrams.programming.framework import React, Vue
from diagrams.programming.language import NodeJS

# ============================================================================ #
# SaaS:
#
#   https://diagrams.mingrammer.com/docs/nodes/saas
#
from diagrams.saas.cdn import Cloudflare

# ============================================================================ #

# https://www.graphviz.org/doc/info/attrs.html
graph_attr = {
    "nodesep": "1",
    "ranksep": "1.5",
    "pad": "0.5",
    "fontsize": "28",
    "labeljust": "c",
    "labelloc": "t",
    "label": "Arquitetura Lifeapps",
    "compound": "true",
    "center": "true",
    # "splines": "spline",  # noqa: ERA001
}

edge_attr = {
    "fontsize": "20",
    "arrowhead": "vee",
    "penwidth": "4",
}

Rest = partial(Edge, color="dodgerblue")
Grpc = partial(Edge, style="dashed", color="firebrick")
GraphQL = partial(Edge, style="dashed", color="pink")
Auth = partial(Edge, style="dashed", color="mediumorchid")
Stream = partial(Edge, style="dashed", color="orange")
Socket = partial(Edge, style="dashed", color="slateblue")
Webhook = partial(Edge, style="dashed", color="mediumseagreen")


def nestjs(label: str) -> Custom:
    """Create a custom node with the NestJS icon."""
    return Custom(label, "../icons/nest.png")


# pylint: disable=W0104,W0106
with Diagram(
    "Arquitetura PAyment",
    show=False,
    direction="TB",
    filename="result/arquitetura_payment",
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

    with Cluster("Cloud"):
        load_balancer = LoadBalancer("K8S Load Balancer")
        dns >> Rest() >> load_balancer
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
            with Cluster("Nginx"):
                nginx_commerce = Nginx("Nginx\nCommerces")
                (
                    nginx
                    >> Rest(
                        lhead="cluster_Ingress",
                    )
                    >> nginx_commerce
                )
                webcommerce = React("WebCommerce")
                custom_webcommerce = React("Custom WebCommerce")
                (
                    nginx_commerce
                    >> Rest(
                        minlen="2",
                    )
                    >> [webcommerce, custom_webcommerce]
                )
            backoffice = Vue("Backoffice")
            cashback = React("Cashback")
            (
                nginx
                >> Rest(
                    ltail="cluster_Ingress",
                    minlen="2",
                )
                >> [
                    cashback,
                    backoffice,
                ]
            )
        with Cluster("Auth"):
            keycloak = Custom("Keycloak", "../icons/keycloak.png")
            (
                nginx
                >> Auth(
                    ltail="cluster_Ingress",
                    lhead="cluster_Auth",
                )
                >> keycloak
            )
            (
                [
                    backoffice,
                    cashback,
                ]
                >> Auth(
                    ltail="cluster_Auth",
                    minlen="2",
                )
                >> keycloak
            )
        with Cluster("Api Gateway"):
            kong = Kong("Kong")
            (
                [
                    webcommerce,
                    custom_webcommerce,
                    cashback,
                    backoffice,
                ]
                >> Rest(
                    lhead="cluster_Api Gateway",
                    minlen="2",
                )
                >> kong
            )
            (
                kong
                >> Auth(
                    ltail="cluster_Api Gateway",
                    lhead="cluster_Auth",
                    minlen="2",
                )
                >> keycloak
            )
        with Cluster("E-commerce"):
            with Cluster("Gateways"):
                cielo = Custom("Cielo", "../icons/cielo.png")
                clearsale = Custom("Clearsale", "../icons/clearsale.png")
                mercadopago = Custom("Mercado Pago", "../icons/mercadopago.png")
                getnet = Custom("Getnet", "../icons/getnet.png")
                paghiper = Custom("Pag Hiper", "../icons/paghiper.png")
                mundipagg = Custom("Mundipagg", "../icons/mundipagg.png")
                efi = Custom("Efí", "../icons/efi.png")
                rede = Custom("Rede", "../icons/rede.png")
                bradesco = Custom("Bradesco", "../icons/bradesco.png")
            # applications
            with Cluster("Payment"):
                payment = NodeJS("Payment")
                payment_db = PostgreSQL("Payment DB")
                payment - payment_db
                (
                    payment
                    >> Rest(
                        lhead="cluster_Gateways",
                        minlen="2",
                    )
                    >> paghiper
                )
                (
                    paghiper
                    >> Webhook(
                        ltail="cluster_Gateways",
                        minlen="2",
                    )
                    >> payment
                )
            with Cluster("Order"):
                order = NodeJS("Order")
                order_db = PostgreSQL("Order DB")
                order - order_db
            with Cluster("Superon Server"):
                server = NodeJS("Superon Server")
                spreadsheet = NodeJS("Spreadsheet")
                redis = Redis("Redis")
                with Cluster("Database"):
                    superon_db_master = PostgreSQL("Superon DB")
                    superon_db_ro = PostgreSQL("Superon DB RO")
                    superon_db_master - superon_db_ro
                server - superon_db_master
        (
            kong
            >> Rest(
                ltail="cluster_Api Gateway",
                minlen="2",
            )
            >> [
                server,
                payment,
                spreadsheet,
                order,
            ]
        )
        with Cluster("Kafka Cluster", graph_attr={"minwidth": "100px"}):
            kafka = Kafka("Broker 01")
            kafka_02 = Kafka("Broker 02")
            kafka_03 = Kafka("Broker 03")
            kafka - [kafka_02, kafka_03]
            (
                [
                    server,
                    payment,
                    spreadsheet,
                    order,
                ]
                >> Stream(
                    lhead="cluster_Message Broker",
                    minlen="2",
                )
                >> kafka
            )
