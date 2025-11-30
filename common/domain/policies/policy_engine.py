# PolicyEngine orchestrates evaluation of multiple policies.
# If any policy returns DENY, the final decision is DENY.

from .policy import PolicyResult


class PolicyEngine:
    def __init__(self, policies=None):
        # List of Policy objects (Strategy pattern)
        self.policies = policies or []

    def add_policy(self, policy):
        self.policies.append(policy)

    def evaluate(self, context):
        """
        Evaluate all policies.
        If ANY policy denies, the action is denied.
        """
        for policy in self.policies:
            result = policy.evaluate(context)
            if result == PolicyResult.DENY:
                return PolicyResult.DENY
        return PolicyResult.ALLOW
