# 2-Player Mario and Luigi Tag Game

A fast-paced **2-player platformer tag game** made with **Python** and **Pygame**, featuring **Mario vs Luigi**, platform movement, jumping, tagging mechanics, and special **ice flower power-ups**.

## Description

This game is a local multiplayer tag game where two players control **Mario** and **Luigi** on a platform map. One player starts as the **tagged player**, and the goal is to avoid being tagged when the timer runs out.

The game also includes an **ice power-up system**:
- Ice flowers spawn around the map
- Players can collect them to gain temporary ice powers
- Ice-powered players can shoot projectiles
- Projectiles freeze the opponent for a short time

The match lasts **60 seconds**, and when the timer ends, the player who is **not tagged** wins.

---

## Features

- 2-player local multiplayer
- Mario and Luigi character sprites
- Platform-based movement and jumping
- Random starting tagged player
- Temporary invincibility after tagging
- Ice flower power-ups
- Ice projectile attacks
- Freeze effect on hit
- Animated walking and jumping sprites
- Game timer and win screen

---

## Controls

### Player 1 — Mario
- **A** → Move left
- **D** → Move right
- **W** → Jump
- **S** → Shoot ice projectile (when ice power is active)

### Player 2 — Luigi
- **Left Arrow** → Move left
- **Right Arrow** → Move right
- **Up Arrow** → Jump
- **Down Arrow** → Shoot ice projectile (when ice power is active)

---

## How the Game Works

- At the start of the game, either Mario or Luigi is randomly chosen as the **tagged player**
- The tagged player is outlined in **yellow**
- If the two players touch, the tag transfers after the invincibility delay ends
- Ice flowers spawn every **15 seconds**
- Collecting an ice flower gives that player **ice power** for **8 seconds**
- Ice power lets the player shoot projectiles
- If a projectile hits the opponent, they are frozen for **1.5 seconds**
- The game ends after **60 seconds**
- The player who is **not tagged** at the end wins

---

## Requirements

Make sure you have Python installed, along with the Pygame library.

### Install Pygame
```bash
pip install pygame
