# Pokémon Gen 3 Style HTML5 Game (Two Phases)

This task requires you to produce a single-file (HTML/CSS/JS) Pokémon Gen 3 style web game, completed in two phases:

## Phase 1 (Prototype Design)
- Tile-based 2D map engine (grass/roads)
- Characters: Player (keyboard arrow keys for movement, using Gen3 protagonist Sprite), NPC (Rival)
- Interaction: Approach NPC and press "Z" to trigger a dialog box; after dialog ends, trigger battle

## Phase 2 (Optimization & Refactoring)
- Add GBA-style encounter battle transition effects (screen flash/blackout/mosaic, etc.)
- Complete battle engine:
  - Background and battle platform
  - Player displays Back Sprite, enemy displays Front Sprite
  - Bottom action panel (Fight/Bag/Run), classic trapezoidal HP bar frame on top
- Gen 3 mechanics (strict):
  - Physical/Special split by type: Special = Fire, Water, Grass, Electric, Psychic, Ice, Dragon, Dark; all others Physical
  - Core damage formula: ((2*Lv/5+2)*Power*A/D)/50+2 (critical hit multiplier 2x; STAB 1.5; type effectiveness 0.5/1/2)
  - Enemy AI: prioritize moves that are super effective against the player; KO if possible; fallback to avoid softlock
- Asset management: Implement AssetLoader/Preloader, prefer PokeAPI Sprites for dynamic loading; display "Loading..." before loading completes; fallback to placeholder on failure
- Interaction & feel: Text character-by-character printing, hit/critical hit/super effective messages, HP bar Lerp animation, hit feedback (shake/flash), input locked during animations

## Resources & References
- Sprite resources (preferred):
  - Enemy front sprite: https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png
  - Player back sprite: https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{id}.png
  - Emerald style (optional): https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/emerald/{id}.png
- Mechanics reference: See context/Reference.docx

## Output Requirements
- Output only a single HTML file (named game.html)
- Code structure should be clear: MapEngine / BattleEngine / GameLoop / AssetManager
- Handle async image loading: Display "Press Start" after resources finish loading

Please generate game.html directly in the working directory.
