from functools import partial  # noqa: INP001

from diagrams import Cluster, Diagram, Edge

# ============================================================================ #
# AWS resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/aws
#
from diagrams.aws.storage import S3
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
from diagrams.elastic.elasticsearch import ElasticSearch

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
from diagrams.programming.language import Go, NodeJS, Python

# ============================================================================ #
# SaaS:
#
#   https://diagrams.mingrammer.com/docs/nodes/saas
#
from diagrams.saas.cdn import Cloudflare
from diagrams.saas.chat import Discord, Messenger, Telegram

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
            menu_unico = Vue("Menu Único")
            faturamento = Vue("Faturamento")
            botinho = React("Botinho")
            paje = Vue("Pajé")
            cashback = React("Cashback")
            (
                nginx
                >> Rest(
                    ltail="cluster_Ingress",
                    minlen="2",
                )
                >> [
                    botinho,
                    cashback,
                    backoffice,
                    menu_unico,
                    paje,
                    faturamento,
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
                    menu_unico,
                    backoffice,
                    faturamento,
                    cashback,
                    botinho,
                ]
                >> Auth(
                    lhead="cluster_Auth",
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
                    botinho,
                    cashback,
                    backoffice,
                    menu_unico,
                    paje,
                    faturamento,
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
        with Cluster("Botinho"):
            api_atendimento = nestjs("API Atendimento")
            api_socket = nestjs("API Socket")
            atendimento_db = PostgreSQL("Atendimento DB")
            with Cluster("Communication Channels"):
                whatsapp = Custom("Whatsapp", "../icons/whatsapp.png")
                telegram_2 = Telegram("Telegram")
                messenger = Messenger("Messenger")
                instagram = Custom("Instagram", "../icons/instagram.png")
            botinho - Socket() - api_socket
            api_atendimento - atendimento_db
            (
                api_atendimento
                >> Rest(
                    lhead="cluster_Communication Channels",
                    minlen="2",
                )
                >> whatsapp
            )
            (
                whatsapp
                >> Webhook(
                    ltail="cluster_Communication Channels",
                    minlen="2",
                )
                >> api_atendimento
            )
        with Cluster("E-commerce"):
            with Cluster("Saas", graph_attr={"bgcolor": "palegreen2"}):
                rd_station = Custom("RD Station", "../icons/rd_station.png")
                with Cluster("Notification", graph_attr={"bgcolor": "palegreen2"}):
                    zenvia = Custom("Zenvia", "../icons/zenvia.png")
                    one_signal = Custom("OneSignal", "../icons/onesignal.png")
                    blip = Custom("Blip", "../icons/blip.png")
                elastic_email = Custom("Elastic Email", "../icons/elastic_email.png")
                telegram = Telegram("Telegram")
                discord = Discord("Discord")

            with Cluster("Gateways", graph_attr={"bgcolor": "palegreen2"}):
                example_gateway = Custom("Example\nGateway", "../icons/gateway.png")

            with Cluster("Transportadoras", graph_attr={"bgcolor": "palegreen2"}):
                correios = Custom("Correios", "../icons/correios.png")
                frenet = Custom("Frenet", "../icons/frenet.png")
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
                    >> example_gateway
                )
                (
                    example_gateway
                    >> Webhook(
                        ltail="cluster_Gateways",
                        minlen="2",
                    )
                    >> payment
                )
            with Cluster("Frete"):
                frete = NodeJS("Frete")
                frete_db = PostgreSQL("Frete DB")
                frete - frete_db
                (
                    frete
                    >> Rest(
                        lhead="cluster_Transportadoras",
                        minlen="2",
                    )
                    >> frenet
                )
            with Cluster("Order"):
                order = NodeJS("Order")
                order_db = PostgreSQL("Order DB")
                order - order_db
            with Cluster("Indexer"):
                indexed_search = NodeJS("Indexed Search")
                pizzaroll = NodeJS("Pizzaroll")
                elastic_search = ElasticSearch("Index\nProducts")
                pizzaroll >> elastic_search
                indexed_search << elastic_search
            with Cluster("Image Proxy"):
                image_proxy = Go("Image Proxy")
                image_bucket = S3("Image\nBucket")
                image_proxy - image_bucket
            with Cluster("IRecommend"):
                irecommend = Python("IRecommend")
                irecommend_helper = Python("IRecommend\nHelper")
                irecommend_db = PostgreSQL("IRecommend DB")
                [irecommend, irecommend_helper] - irecommend_db
            with Cluster("Banners"):
                banner = nestjs("Banner\nService")
                banner_db = PostgreSQL("Banner DB")
                banner_bucket = S3("Banner\nBucket")
                banner - [banner_db, banner_bucket]
            with Cluster("Authenticator"):
                authenticator = nestjs("Authenticator")
                authenticator_db = PostgreSQL("Auth DB")
                authenticator - authenticator_db
            with Cluster("Dados Públicos"):
                dadospublicos = NodeJS("Dados Públicos")
                cep_db = PostgreSQL("CEP DB")
                dadospublicos - cep_db
            with Cluster("Notification"):
                message_job = Python("Message Job")
                prupru = NodeJS("Prupru")
                telebot = NodeJS("Telebot")
                telegram_db = PostgreSQL("Telegram DB")
                telebot - telegram_db
                email_db = PostgreSQL("Email DB")
                rd_station_db = PostgreSQL("RD Station DB")
                [message_job, prupru] - email_db
                rdstation_notifier = NodeJS("RDStation Notifier")
                rdstation_notifier - rd_station_db
                message_notifier = NodeJS("Message Notifier")
                notifier_db = PostgreSQL("Notifier DB")
                message_notifier - notifier_db
            with Cluster("Superon Server"):
                server = NodeJS("Superon Server")
                spreadsheet = NodeJS("Spreadsheet")
                redis = Redis("Redis")
                with Cluster("Database"):
                    superon_db_master = PostgreSQL("Superon DB")
                    superon_db_ro = PostgreSQL("Superon DB RO")
                    superon_db_master - superon_db_ro
                server - superon_db_master
                server - redis
            with Cluster("Integração"):
                paje = Go("Pajé")
                paje_db = PostgreSQL("Pajé DB")
                paje - paje_db
            with Cluster("Chateado"):
                chateado = NodeJS("Chateado")
                (chateado >> Grpc() >> server)
            [webcommerce, custom_webcommerce] - Socket() - chateado
            (
                message_notifier
                >> Rest(
                    lhead="cluster_Notification",
                    minlen="2",
                )
                >> one_signal
            )
            rdstation_notifier >> Rest() >> rd_station
            telebot >> Rest() >> telegram
            message_job >> Rest() >> elastic_email
            server >> Webhook() >> discord
            server >> Grpc() >> paje
            paje >> Rest() >> server
        with Cluster("Cashback"):
            cashback_api = nestjs("Cashback Api")
            cashback_db = PostgreSQL("Cashback DB")
            cashback_api - cashback_db
        with Cluster("Menu Único"):
            menu_unico_api = NodeJS("Menu Único API")
            faturamento = NodeJS("Faturamento")
            faturamento_db = PostgreSQL("Faturamento DB")
            faturamento - faturamento_db
            (
                [faturamento, menu_unico_api]
                >> Auth(
                    lhead="cluster_Auth",
                    minlen="2",
                )
                >> keycloak
            )
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
                banner,
                menu_unico_api,
                api_atendimento,
                cashback_api,
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
                    irecommend,
                    irecommend_helper,
                    chateado,
                    faturamento,
                    prupru,
                    image_proxy,
                    banner,
                    api_atendimento,
                    api_socket,
                    cashback_api,
                ]
                >> Stream(
                    lhead="cluster_Message Broker",
                    minlen="2",
                )
                >> kafka
            )
