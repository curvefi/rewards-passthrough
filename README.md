## Passthrough Contract

The Passthrough contract is designed to facilitate reward token distribution on L2 networks acting as an intermediary for depositing reward tokens to authorized gauge contracts.

### Overview

This contract serves as a secure passthrough mechanism that allows authorized distributors and guards to deposit reward tokens to designated gauge contracts.


### Key Features

- **Role-Based Access Control**
  - Guards: Can manage distributors and other guards
  - Distributors: Can deposit reward tokens, Guards are also distributors
  - Non-removable Guards: Special guard addresses that cannot be removed (OWNERSHIP_ADMIN and PARAMETER_ADMIN)
  - OWNERSHIP_ADMIN and PARAMETER_ADMIN are set to the curve agent

### Administrative Functions

- `add_guard`: Add new guard addresses
- `remove_guard`: Remove existing guards (except non-removable ones)
- `add_distributor`: Add new distributor addresses
- `remove_distributor`: Remove existing distributors
- `set_single_reward_receiver`: Set the default gauge for reward deposits

### Security Features

1. Guards cannot remove themselves
2. Core admin addresses are set as non-removable guards
3. Role-based access control for all administrative functions

### Usage

1. Deploy the contract with initial reward receivers (currently not used, set to []), guards, and distributors
2. Guards can manage the system by adding/removing other guards and distributors
3. Set a single reward receiver (gauge) for simplified deposits
4. Authorized distributors or guards can deposit reward tokens either to:
   - The pre-configured single receiver
   - Any specified gauge address

### Events

The contract emits events for all significant actions:
- `PassthroughDeployed`
- `SetSingleRewardReceiver`
- `AddGuard`
- `RemoveGuard`
- `AddDistributor`
- `RemoveDistributor`
- `SentRewardToken`
- `SentRewardTokenWithReceiver`

### Limitations

- Maximum of 10 guards
- Maximum of 10 distributors
- Maximum of 10 reward receivers in the initial array (currently not used)
- Reward receivers must be compatible gauge contracts
