6. COIN ENTITIES
# =============================================================================
class Coin:
    def __init__(self, x, y, kind="regular"):
        self.x, self.y = x, y
        self.kind = kind
        self.spin_angle = random.uniform(0, math.pi * 2)
        self.bob_offset = random.uniform(0, math.pi * 2)
        self.radius = 16 if kind == "regular" else (20 if kind == "super" else 18)
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self, road_speed, player=None):
        self.spin_angle = (self.spin_angle + 0.11) % (math.pi * 2)
        self.bob_offset += 0.08

        if player and player.has_magnet:
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy)
            magnet_range = 340 if getattr(player, "car_data", {}).get("id") == 3 else 240
            if dist < magnet_range:
                pull_speed = max(9.0, (magnet_range - dist) * 0.16)
                self.x += (dx / dist) * pull_speed
                self.y += (dy / dist) * pull_speed

        self.y += road_speed
        self.hitbox.center = (int(self.x), int(self.y))

    def draw(self, surface):
        draw_y = self.y + math.sin(self.bob_offset) * 4
        spin_scale = abs(math.cos(self.spin_angle))
        coin_w = max(4, int(self.radius * 2 * spin_scale))
        coin_h = self.radius * 2

        if self.kind == "regular":
            halo_surf = pygame.Surface((self.radius * 3, self.radius * 3), pygame.SRCALPHA)
            pygame.draw.circle(halo_surf, (245, 158, 11, 45), (self.radius * 3 // 2, self.radius * 3 // 2), int(self.radius * 1.3))
            surface.blit(halo_surf, (self.x - self.radius * 3 // 2, draw_y - self.radius * 3 // 2))

            c_surf = pygame.Surface((coin_w + 4, coin_h + 4), pygame.SRCALPHA)
            rect = pygame.Rect(2, 2, coin_w, coin_h)
            pygame.draw.ellipse(c_surf, (217, 119, 6), rect)
            pygame.draw.ellipse(c_surf, (251, 191, 36), (rect.x + 1, rect.y + 1, max(2, rect.width - 2), max(2, rect.height - 2)))
            pygame.draw.ellipse(c_surf, COLOR_GOLD_LIGHT, (rect.x + 2, rect.y + 3, max(2, rect.width // 2), max(2, rect.height // 3)))
            surface.blit(c_surf, (self.x - coin_w // 2 - 2, draw_y - coin_h // 2 - 2))

        elif self.kind == "super":
            halo_surf = pygame.Surface((self.radius * 3, self.radius * 3), pygame.SRCALPHA)
            pygame.draw.circle(halo_surf, (168, 85, 247, 65), (self.radius * 3 // 2, self.radius * 3 // 2), int(self.radius * 1.4))
            surface.blit(halo_surf, (self.x - self.radius * 3 // 2, draw_y - self.radius * 3 // 2))

            c_surf = pygame.Surface((coin_w + 4, coin_h + 4), pygame.SRCALPHA)
            rect = pygame.Rect(2, 2, coin_w, coin_h)
            pygame.draw.ellipse(c_surf, (147, 51, 234), rect)
            pygame.draw.ellipse(c_surf, (245, 158, 11), (rect.x + 2, rect.y + 2, max(2, rect.width - 4), max(2, rect.height - 4)))
            pygame.draw.ellipse(c_surf, (239, 68, 68), (rect.x + 4, rect.y + 4, max(2, rect.width - 8), max(2, rect.height - 8)))
            surface.blit(c_surf, (self.x - coin_w // 2 - 2, draw_y - coin_h // 2 - 2))

        elif self.kind == "magnet":
            m_surf = pygame.Surface((38, 38), pygame.SRCALPHA)
            pygame.draw.circle(m_surf, (6, 182, 212, 70), (19, 19), 18)
            pygame.draw.arc(m_surf, (239, 68, 68), (6, 6, 26, 26), 0, math.pi, 6)
            pygame.draw.rect(m_surf, (240, 240, 240), (6, 17, 6, 8))
            pygame.draw.rect(m_surf, (240, 240, 240), (26, 17, 6, 8))
            surface.blit(m_surf, (self.x - 19, draw_y -19))
