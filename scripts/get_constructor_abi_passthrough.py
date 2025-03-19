from ape import project
from eth_abi import encode


def get_constructor_args(*args):
    """
    Get encoded constructor arguments for Passthrough contract
    Args:
        *args: Variable length argument list containing:
            - agents: list of agent addresses
            - rewards_tokens: list of reward token addresses
            - rewards_contracts: list of reward contract addresses
            - distributors: list of distributor addresses
    """
    # Get constructor ABI
    constructor = next(
        item for item in project.Passthrough.contract_type.abi if item.type == "constructor"
    )

    # Get the constructor input types
    input_types = [arg.type for arg in constructor.inputs]

    # Use passed arguments or default values
    if args:
        constructor_args = args
    else:
        # Default values if no args provided
        distributors = [
            "0x9f499A0B7c14393502207877B17E3748beaCd70B",
            "0x84bC1fC6204b959470BF8A00d871ff8988a3914A",
        ]
        constructor_args = [[], [], distributors]

    # Encode the arguments
    encoded_args = encode(input_types, constructor_args)
    print("Encoded constructor arguments:", encoded_args.hex())


if __name__ == "__main__":
    get_constructor_args()
