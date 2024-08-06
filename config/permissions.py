


ROLES_PERMISSIONS = {
    "sales": ["create-client", "list-clients", "update-contract", "update-client", "delete-client", "list-contracts",
              "create-event", "list-collaborators","list-unpaid-contracts","list-unsigned-contracts" ],
    "support": ["list-collaborators", "list-contracts", "list-clients", "list-events", "update-event"],
    "management": ["create-contract", "create-collaborator", "delete-collaborator", "list-collaborators",
                   "update-collaborator", "list-contracts", "list-clients", "list-events", "create-contract",
                   "update-contract", "delete-contract", "update-event", "delete-event",],
}


def is_support(collaborator):
    return collaborator.role.name == "support"

def is_management(collaborator):
    return collaborator.role.name == "management"

def is_sales(collaborator):
    return collaborator.role.name == "sales"
