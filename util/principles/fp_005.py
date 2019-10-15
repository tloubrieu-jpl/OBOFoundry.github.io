#!/usr/bin/env python

## ## "Scope" Automated Check
##
## ### Requirements
## 1. A scope ('domain') **must** be declared in the registry data
## 2. Registry ontologies *should* cover non-overlapping domains
##
## ### Implementation
## First, the registry data is checked for a 'domain' tag. If missing, that is an error. If it is present, the domain is compared to all other ontology domains. If the ontology shares a domain with one or more other ontologies, we return a list of those ontologies in an info message.

import dash_utils
from dash_utils import format_msg

info_msg = 'shares domain \'{0}\' with: {1}'


def has_scope(data, domain_map):
    '''Check fp 5 - scope.

    Retrieve the "scope" tag from the data and compare to other scopes in the
    map. If domains overlap, return INFO with a list of overlapping domains.
    If scope is missing, ERROR. Otherwise, PASS.

    Args:
        data (dict): ontology data from registry
        domain_map (dict): map of ontology to domain
    '''
    ns = data['id']
    if 'domain' in data:
        domain = data['domain']
    else:
        return format_msg('ERROR', ['missing domain (scope)'])

    # exclude this NS from check (it will match itself)
    updated_domain_map = domain_map
    updated_domain_map.pop(ns)

    if domain in updated_domain_map.values():
        same_domain = []
        for ont_id, other_domain in domain_map.items():
            if domain == other_domain:
                same_domain.append(ont_id)
        same_domain_str = " ".join(same_domain)
        return format_msg('INFO', [info_msg.format(domain, same_domain_str)])

    return 'PASS'