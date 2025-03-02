#pragma version ^0.4.0
"""
@title Passthrough for L2
@author anon contributor to curve
@license MIT
@notice passthrough contract who can deposit token rewards to allowed reward_receivers (gauges)
"""

from ethereum.ercs import IERC20

interface Gauge:
    def deposit_reward_token(_reward_token: address, _amount: uint256, _epoch: uint256): nonpayable
    def reward_data(_token: address) -> (address, uint256): view
    def manager() -> address: view

# hardcoded addresses for Taiko
# L2 OWNERSHIP ADMIN 
OWNERSHIP_ADMIN: constant(address) = 0x6c9578402A3ace046A12839f45F84Aa5448E9c30
# L2 PARAMETER_ADMIN
PARAMETER_ADMIN: constant(address) = 0xEC5AFc9590964f2fA0FeED54f0fBB2A34480908D

FIRST_GUARD: constant(address) = 0x9f499A0B7c14393502207877B17E3748beaCd70B

WEEK: public(constant(uint256)) = 7 * 24 * 60 * 60  # 1 week in seconds

guards: public(DynArray[address, 10])  # L2 guards
non_removable_guards: public(DynArray[address, 2])  # L2 fixed guards
distributors: public(DynArray[address, 10])  # L2 distributors
reward_receivers: public(DynArray[address, 10])  # L2 reward receivers
single_reward_receiver: public(address)
single_reward_token: public(address)

name: public(String[128])

event PassthroughDeployed:
    timestamp: uint256

event SetSingleRewardReceiver:
    single_reward_receiver: address
    timestamp: uint256

event SetSingleRewardToken:
    single_reward_token: address
    timestamp: uint256

event SetName:
    name: String[128]
    timestamp: uint256

event AddGuard:
    new_guard: address
    timestamp: uint256

event RemoveGuard:
    removed_guard: address
    timestamp: uint256

event AddDistributor:
    new_distributor: address
    timestamp: uint256

event RemoveDistributor:
    removed_distributor: address
    timestamp: uint256

event SentRewardToken:
    single_reward_receiver: address
    reward_token: address
    amount: uint256
    epoch: uint256
    timestamp: uint256

event SentRewardTokenWithReceiver:
    reward_receiver: address
    reward_token: address
    amount: uint256
    epoch: uint256
    timestamp: uint256

@deploy
def __init__(_reward_receivers: DynArray[address, 10], _guards: DynArray[address, 7], _distributors: DynArray[address, 10]):
    """
    @notice Contract constructor
    @param _reward_receivers Reward receivers addresses, currently not used anywhere!
    @param _guards Guards addresses
    @param _distributors Distributors addresses
    @dev _reward_receivers are not used anywhere, as the sending reward is gated by the depositor address in the gauge (this contract)
    """
    self.reward_receivers = _reward_receivers
    self.guards = _guards
    # add default guards
    self.guards.append(FIRST_GUARD)
    self.guards.append(OWNERSHIP_ADMIN)
    self.guards.append(PARAMETER_ADMIN)
    
    self.non_removable_guards.append(OWNERSHIP_ADMIN)
    self.non_removable_guards.append(PARAMETER_ADMIN)

    
    self.distributors = _distributors

    log PassthroughDeployed(block.timestamp)


@external
def deposit_reward_token(_reward_token: address, _amount: uint256, _epoch: uint256 = WEEK):
    """
    @notice Deposit reward token
    @param _reward_token Reward token address
    @param _amount Amount of reward token to deposit
    @param _epoch Epoch to deposit reward token, default is 1 week in seconds, min. 3 days in L2 gauges
    @dev This function is used to deposit reward token to the single reward receiver
    @dev To use this function, set the single reward receiver first (gauge address)
    """
    assert msg.sender in self.distributors or msg.sender in self.guards, 'only distributors or guards can call this function'
    assert self.single_reward_receiver != ZERO_ADDRESS, 'single reward receiver not set'

    assert extcall IERC20(_reward_token).transferFrom(msg.sender, self, _amount)
    assert extcall IERC20(_reward_token).approve(self.single_reward_receiver, _amount)

    extcall Gauge(self.single_reward_receiver).deposit_reward_token(_reward_token, _amount, _epoch)

    log SentRewardToken(self.single_reward_receiver, _reward_token, _amount, _epoch, block.timestamp)  


@external
def deposit_reward(_amount: uint256, _epoch: uint256 = WEEK):
    """
    @notice Deposit reward token
    @param _amount Amount of reward token to deposit
    @param _epoch Epoch to deposit reward token, default is 1 week in seconds, min, 3 days in L2 gauges
    @dev This function is used to deposit reward token to the single reward receiver with a fixed reward token
    @dev To use this function, set the single reward receiver first (gauge address)
    """
    assert msg.sender in self.distributors or msg.sender in self.guards, 'only distributors or guards can call this function'
    assert self.single_reward_token != ZERO_ADDRESS, 'single reward token not set'
    assert self.single_reward_receiver != ZERO_ADDRESS, 'single reward receiver not set'

    assert extcall IERC20(self.single_reward_token).transferFrom(msg.sender, self, _amount)
    assert extcall IERC20(self.single_reward_token).approve(self.single_reward_receiver, _amount)

    extcall Gauge(self.single_reward_receiver).deposit_reward_token(self.single_reward_token, _amount, _epoch)

    log SentReward(self.single_reward_receiver, _reward_token, _amount, _epoch, block.timestamp)


@external
def set_single_reward_receiver(_single_reward_receiver: address):
    """
    @notice Set the single reward receiver
    @param _single_reward_receiver The address of the single reward receiver
    @dev This can be used to set a single reward receiver to have the deposit_reward_token()
    @dev function the same interface as in a gauge
    """
    assert msg.sender in self.guards, 'only guards can call this function'
    self.single_reward_receiver = _single_reward_receiver

    log SetSingleRewardReceiver(_single_reward_receiver, block.timestamp)

@external
def set_single_reward_token(_single_reward_token: address):
    """
    @notice Set the single reward token
    @param _single_reward_token The address of the single reward token
    @dev This can be used to set a single reward token to have the deposit_reward()
    @dev function the same interface as in a gauge
    """
    assert msg.sender in self.guards, 'only guards can call this function'
    self.single_reward_token = _single_reward_token

    log SetSingleRewardToken(_single_reward_token, block.timestamp)


@external
def deposit_reward_token_with_receiver(_reward_receiver: address, _reward_token: address, _amount: uint256, _epoch: uint256 = WEEK):
    """
    @notice Deposit reward token
    @param _reward_receiver Reward receiver address
    @dev reward receiver must be a gauge, as access is set as depositor in the gauge, this is not to be gated here
    @param _reward_token Reward token address
    @param _amount Amount of reward token to deposit
    @param _epoch Epoch to deposit reward token
    """
    assert msg.sender in self.distributors or msg.sender in self.guards, 'only distributors or guards can call this function'
    
    assert extcall IERC20(_reward_token).transferFrom(msg.sender, self, _amount)
    assert extcall IERC20(_reward_token).approve(_reward_receiver, _amount)

    extcall Gauge(_reward_receiver).deposit_reward_token(_reward_token, _amount, _epoch)

    log SentRewardTokenWithReceiver(_reward_receiver, _reward_token, _amount, _epoch, block.timestamp)  

@view
@external
def reward_data(_reward_receiver: address, _token: address) -> (address, uint256):
    return staticcall Gauge(_reward_receiver).reward_data(_token)


@external
def add_distributor(_new_distributor: address):
    # assert msg.sender in [Gauge(self.reward_receiver).manager(), PARAMETER_ADMIN, OWNERSHIP_ADMIN]

    assert msg.sender in self.guards, 'only guards can call this function'
    assert _new_distributor not in self.distributors, 'prevent to add the same distributor twice'

    self.distributors.append(_new_distributor)

    log AddDistributor(_new_distributor, block.timestamp)

@external
def remove_distributor(_rm_distributor: address):
    """
    @notice Remove an active campaign address from the list
    @param _rm_distributor The address of the distributor to remove
    @dev todo: now a distributor not in the list also creats the RemoveDistributor event
    """
    assert msg.sender in self.guards, 'only guards can call this function'
    
    for i: uint256 in range(len(self.distributors), bound=10):
        if self.distributors[i] == _rm_distributor:    
            last_idx: uint256 = len(self.distributors) - 1
            if i != last_idx:
                self.distributors[i] = self.distributors[last_idx]
            self.distributors.pop()
            break

    log RemoveDistributor(_rm_distributor, block.timestamp)


@external
def add_guard(_new_guard: address):
    # assert msg.sender in [Gauge(self.reward_receiver).manager(), PARAMETER_ADMIN, OWNERSHIP_ADMIN]

    assert msg.sender in self.guards, 'only guards can call this function'
    assert _new_guard not in self.guards, 'prevent to add the same guard twice'

    self.guards.append(_new_guard)

    log AddGuard(_new_guard, block.timestamp)

@external
def remove_guard(_rm_guard: address):
    """
    @notice Remove an active guard address from the list
    @param _rm_guard The address of the guard to remove
    """
    assert msg.sender in self.guards, 'only guards can call this function'
    assert _rm_guard != msg.sender, 'guards cannot remove themselves'
    assert _rm_guard not in self.non_removable_guards, 'non-removable guards cannot be removed'
    
    for i: uint256 in range(len(self.guards), bound=10):
        if self.guards[i] == _rm_guard:    
            last_idx: uint256 = len(self.guards) - 1
            if i != last_idx:
                self.guards[i] = self.guards[last_idx]
            self.guards.pop()
            break

    log RemoveGuard(_rm_guard, block.timestamp)


@external
def set_name(name: String[128]):
    """
    @notice Set the name of the passthrough contract
    @param name The name of the passthrough contract
    """
    assert msg.sender in self.guards, 'only guards can call this function'
    self.name = name

    log SetName(name, block.timestamp)


@external
@view
def get_all_reward_receivers() -> DynArray[address, 10]:
    """
    @notice Get all guards
    @return DynArray[address, 10] Array containing all guards
    """
    return self.reward_receivers

@external
@view
def get_all_guards() -> DynArray[address, 10]:
    """
    @notice Get all guards
    @return DynArray[address, 10] Array containing all guards
    """
    return self.guards

@external
@view
def get_all_distributors() -> DynArray[address, 10]:
    """
    @notice Get all distributors
    @return DynArray[address, 10] Array containing all distributors
    """
    return self.distributors
