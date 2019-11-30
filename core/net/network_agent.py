#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importing Custom Logger & Logging Modules

# Import Socket Exceptions
from core.net.exceptions.network_exceptions import (NetworkAgentFatalException)

# Import Socket Module
import socket
from gnosis.eth.ethereum_client import EthereumClient


DEFAULT_INFURA_API_KEY =  'b3fa360a82cd459e8f1b459b3cf9127c'
DEFAULT_ETHERSCAN_API_KEY = 'A1T1PKJXZJC1T4RJZK4ZMZH4JEYTUGAA6G'

class NetworkAgent:
    """ Network Agent

    Code Reference: https://stackoverflow.com/questions/3764291/checking-network-connection
    This class will establish the current state of the connectivity to internet for the system in case it's needed.
    """
    def __init__(self, logger, network='ganache', api_key=None):
        self.name = self.__class__.__name__
        self.logger = logger
        self.network = network
        self.ethereum_client = None

        # Default Polling Address Settings: Used for checking internet availability
        self.polling_address = '8.8.8.8'
        self.polling_port = 53
        self.polling_timeout = 3

        # Default Ethereum Node Endpoint for the EthereumClient
        self.default_node_endpoint = 'http://localhost:8545'
        self.current_node_endpoint = ''
        if self.network_status():
            self.set_network_provider_endpoint(network, api_key)

    def _setup_new_provider(self, node_url):
        """ Setup New Provider

        This function will setup the proper provider based on the node_url, if it's connected it will setup the
            :param node_url:
            :return: self.ethereum_client, othewise it will return an error
        """
        tmp_client = EthereumClient(ethereum_node_url=node_url)
        if tmp_client.w3.isConnected():
            self.ethereum_client = tmp_client
            self.logger.info('{0} Successfully retrieved a valid connection to {1} '.format(self.name, node_url))
        else:
            self.logger.error('{0} Unable to retrieve a valid connection to {1} '.format(self.name, node_url))

    def get_current_node_endpoint(self):
        """ Get Current Node Endpoint

        This function will return the current node endpoint url
            :return:
        """
        return self.current_node_endpoint

    def get_ethereum_client(self):
        """ Get Ethereum Client

        This function will retrieve and return the current EthereumClient
            :return:
        """
        return self.ethereum_client

    def command_view_networks(self):
        """ Command View Networks

        This function will retrieve and show the current network used by the ethereum client
            :return:
        """
        self.logger.debug0('---------'*10)
        self.logger.info(' | Network Status: {0} | '.format(self.network_status()))
        self.logger.info(' | Connected to {0} Through {1} | '.format(self.network.title(), self.current_node_endpoint))
        self.logger.debug0('---------'*10)

    def set_network_provider_endpoint(self, network, api_key=None):
        """ Set Network

        This function will set the current enpoint for the ethereum client
            :param network:
            :param api_key:
            :return:
        """
        if network == 'mainnet':
            mainnet_node_url = '{0}{1}'.format('https://mainnet.infura.io/v3/', api_key)
            if api_key is not None:
                self._setup_new_provider(mainnet_node_url)
                self.network = 'mainnet'
                self.current_node_endpoint = mainnet_node_url
            else:
                self.logger.error('Infura API KEY needed, {0} Unable to retrieve a valid connection to {1} '.format(self.name, mainnet_node_url))

        elif network == 'ropsten':
            ropsten_node_url = '{0}{1}'.format('https://ropsten.node.url/', api_key)
            if api_key is not None:
                self._setup_new_provider(ropsten_node_url)
                self.network = 'ropsten'
                self.current_node_endpoint = ropsten_node_url
            else:
                self.logger.error('API KEY needed, {0} Unable to retrieve a valid connection to {1} '.format(self.name, ropsten_node_url))

        elif network == 'rinkeby':
            rinkeby_node_url = '{0}{1}'.format('https://rinkeby.infura.io/v3/', api_key)
            if api_key is not None:
                self._setup_new_provider(rinkeby_node_url)
                self.network = 'rinkeby'
                self.current_node_endpoint = rinkeby_node_url
            else:
                self.logger.error('API KEY needed, {0} Unable to retrieve a valid connection to {1} '.format(self.name, rinkeby_node_url))
        elif network == 'ganache':
            self._setup_new_provider(self.default_node_endpoint)
            self.network = 'ganache'
            self.current_node_endpoint = self.default_node_endpoint

    def network_status(self):
        """ Network Status

        This Function will check the availability of the network connection
            :return True if there is internet connectivity otherwise False
        """
        try:
            socket.setdefaulttimeout(self.polling_timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.polling_address, self.polling_port))
            return True
        except socket.error:
            return False
        except Exception as err:
            # Empty param should be trace for further debugging in case it's needed
            self.logger.error('{0}: Something went really wrong: {1}'.format(self.name, err))
            raise NetworkAgentFatalException(self.name, err, '')