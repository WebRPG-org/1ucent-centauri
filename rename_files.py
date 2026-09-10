#!/usr/bin/env python3
"""
Script to rename game files in the assets/UGS directory.
Maps file names to clean game titles and renames accordingly.
"""

import os
import json
import re
from pathlib import Path

# Game mapping: filename -> clean title
GAME_MAPPING = {
    # 1-9 section
    "cl1.html": "1-91.html",
    "cl10bullets.html": "10-Bullets.html",
    "cl10minutestildawn.html": "10-Minutes-Till-Dawn.html",
    "cl10morebullets.html": "10-More-Bullets.html",
    "cl10yardfight.html": "10-Yard-Fight.html",
    "cl12minibattles.html": "12-Mini-Battles.html",
    "cl13bones.html": "13-Bones.html",
    "cl1on1soccer.html": "1-on-1-Soccer.html",
    "cl1v1lol.html": "1v1-LOL.html",
    "cl1v1tennis.html": "1v1-Tennis.html",
    "cl100RoomsOfEnemies.html": "100-Rooms-of-Enemies.html",
    "cl100in1nes.html": "100-in-1-NES.html",
    "cl20smallmazes.html": "20-Small-Mazes.html",
    "cl2048.html": "2048.html",
    "cl2048cupcakes.html": "2048-Cupcakes.html",
    "cl234playergame.html": "2-3-4-Player-Mini-Games.html",
    "cl2Dshooting.html": "2D-Shooting.html",
    "cl2doom.html": "2-Doom.html",
    "cl3dash.html": "3-Dash.html",
    "cl3dasheditor.html": "3-Dash-Editor.html",
    "cl3dpinballspacecadet.html": "3D-Pinball-Space-Cadet.html",
    "cl3pandas.html": "3-Pandas.html",
    "cl3pandasbrazil.html": "3-Pandas-in-Brazil.html",
    "cl3pandasfantasy.html": "3-Pandas-in-Fantasy.html",
    "cl3pandasjapan.html": "3-Pandas-in-Japan.html",
    "cl3pandasnight.html": "3-Pandas-Night.html",
    "cl3slices2.html": "3-Slices-2.html",
    "cl40xescape.html": "40x-Escape.html",
    "cl4thandgoal.html": "4th-and-Goal.html",
    "cl500calibercontractz.html": "500-Caliber-Contractz.html",
    "cl60secondsburgerrun.html": "60-Seconds-Burger-Run.html",
    "cl60secondssantarun.html": "60-Seconds-Santa-Run.html",
    "cl64in1nes.html": "64-in-1-NES.html",
    "cl8ballclassic.html": "8-Ball-Classic.html",
    "cl8ballpool.html": "8-Ball-Pool.html",
    "cl90in1nes.html": "90-in-1-NES.html",
    "cl99balls.html": "99-Balls.html",
    "cl99nightsitf.html": "99-Nights-in-the-Forest.html",
    "cl9007199254740992.html": "9007199254740992.html",
}

def sanitize_filename(name: str) -> str:
    """
    Sanitize a filename by:
    - Replacing spaces with hyphens
    - Removing special characters
    - Converting to lowercase (optional)
    """
    # Replace spaces with hyphens
    name = name.replace(" ", "-")
    # Remove invalid filesystem characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name

def rename_files(directory: str, dry_run: bool = True) -> dict:
    """
    Rename files in directory based on mapping.
    
    Args:
        directory: Path to directory containing files
        dry_run: If True, only print changes without making them
        
    Returns:
        dict with statistics about the operation
    """
    results = {
        "renamed": [],
        "skipped": [],
        "errors": [],
        "total": 0
    }
    
    path = Path(directory)
    
    if not path.exists():
        results["errors"].append(f"Directory not found: {directory}")
        return results
    
    # Get all HTML files
    html_files = sorted(path.glob("*.html"))
    results["total"] = len(html_files)
    
    print(f"Found {len(html_files)} HTML files in {directory}\n")
    
    for old_path in html_files:
        old_name = old_path.name
        
        # Check if file has a mapping
        if old_name in GAME_MAPPING:
            new_name = GAME_MAPPING[old_name]
            new_path = path / new_name
            
            # Avoid overwriting
            if new_path.exists() and new_path != old_path:
                msg = f"SKIP: {old_name} -> {new_name} (target exists)"
                results["skipped"].append(msg)
                print(f"⚠️  {msg}")
            else:
                if dry_run:
                    print(f"[DRY RUN] RENAME: {old_name} -> {new_name}")
                else:
                    try:
                        old_path.rename(new_path)
                        results["renamed"].append((old_name, new_name))
                        print(f"✓ RENAMED: {old_name} -> {new_name}")
                    except Exception as e:
                        error_msg = f"ERROR renaming {old_name}: {str(e)}"
                        results["errors"].append(error_msg)
                        print(f"✗ {error_msg}")
        else:
            results["skipped"].append(old_name)
    
    return results

def print_statistics(results: dict, dry_run: bool = True):
    """Print operation statistics."""
    print(f"\n{'='*60}")
    print(f"OPERATION: {'DRY RUN' if dry_run else 'ACTUAL RENAME'}")
    print(f"{'='*60}")
    print(f"Total files found: {results['total']}")
    print(f"Files renamed: {len(results['renamed'])}")
    print(f"Files skipped: {len(results['skipped'])}")
    print(f"Errors: {len(results['errors'])}")
    
    if results["errors"]:
        print(f"\n⚠️  ERRORS ({len(results['errors'])}):")
        for error in results["errors"][:10]:  # Show first 10
            print(f"  - {error}")
    
    if results["renamed"]:
        print(f"\n✓ RENAMED ({len(results['renamed'])}):")
        for old, new in results["renamed"][:10]:  # Show first 10
            print(f"  {old} -> {new}")

def main():
    """Main entry point."""
    # Directory containing game files
    game_dir = "assets/UGS"
    
    print("🎮 Game File Rename Script")
    print(f"Target directory: {game_dir}\n")
    
    # First, run dry run
    print("📋 Running DRY RUN first...\n")
    dry_results = rename_files(game_dir, dry_run=True)
    print_statistics(dry_results, dry_run=True)
    
    # Ask for confirmation
    print("\n" + "="*60)
    response = input("\nProceed with actual rename? (yes/no): ").strip().lower()
    
    if response in ["yes", "y"]:
        print("\n🔄 Proceeding with actual rename...\n")
        actual_results = rename_files(game_dir, dry_run=False)
        print_statistics(actual_results, dry_run=False)
        print("\n✅ Rename operation complete!")
    else:
        print("\n❌ Rename cancelled. No files were modified.")

if __name__ == "__main__":
    main()
