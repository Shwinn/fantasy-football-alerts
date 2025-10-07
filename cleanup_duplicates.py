#!/usr/bin/env python3
"""
Script to detect and clean up duplicate articles created before deduplication system.
"""

import os
import hashlib
from collections import defaultdict
from datetime import datetime


def get_file_hash(filepath):
    """Calculate MD5 hash of file content."""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def get_article_title(filepath):
    """Extract title from article file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith('Title: '):
                return first_line[7:]  # Remove 'Title: ' prefix
    except Exception as e:
        print(f"Error reading title from {filepath}: {e}")
    return "Unknown"


def find_duplicates(articles_dir="scraped_articles"):
    """Find duplicate articles based on content hash and title."""
    if not os.path.exists(articles_dir):
        print(f"Articles directory '{articles_dir}' not found.")
        return
    
    print("Scanning for duplicate articles...")
    print("=" * 50)
    
    # Group files by content hash
    hash_groups = defaultdict(list)
    # Group files by title
    title_groups = defaultdict(list)
    
    total_files = 0
    
    # Walk through all article files
    for root, dirs, files in os.walk(articles_dir):
        for filename in files:
            if filename.endswith('.txt'):
                filepath = os.path.join(root, filename)
                total_files += 1
                
                # Get content hash
                file_hash = get_file_hash(filepath)
                if file_hash:
                    hash_groups[file_hash].append(filepath)
                
                # Get title for grouping
                title = get_article_title(filepath)
                title_groups[title].append(filepath)
    
    print(f"Scanned {total_files} article files")
    print()
    
    # Find duplicates by content hash
    content_duplicates = {h: files for h, files in hash_groups.items() if len(files) > 1}
    
    # Find duplicates by title
    title_duplicates = {t: files for t, files in title_groups.items() if len(files) > 1 and t != "Unknown"}
    
    print("DUPLICATE ANALYSIS")
    print("=" * 50)
    
    if content_duplicates:
        print(f"Found {len(content_duplicates)} groups of identical content:")
        for i, (file_hash, files) in enumerate(content_duplicates.items(), 1):
            print(f"\n{i}. Content Hash: {file_hash[:12]}...")
            for j, filepath in enumerate(files):
                rel_path = os.path.relpath(filepath, articles_dir)
                file_size = os.path.getsize(filepath)
                mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                print(f"   {j+1}. {rel_path} ({file_size} bytes, {mod_time.strftime('%Y-%m-%d %H:%M')})")
    else:
        print("No identical content duplicates found.")
    
    print()
    
    if title_duplicates:
        print(f"Found {len(title_duplicates)} groups of articles with same title:")
        for i, (title, files) in enumerate(title_duplicates.items(), 1):
            print(f"\n{i}. Title: {title[:60]}{'...' if len(title) > 60 else ''}")
            for j, filepath in enumerate(files):
                rel_path = os.path.relpath(filepath, articles_dir)
                file_size = os.path.getsize(filepath)
                mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                print(f"   {j+1}. {rel_path} ({file_size} bytes, {mod_time.strftime('%Y-%m-%d %H:%M')})")
    else:
        print("No title duplicates found.")
    
    return content_duplicates, title_duplicates


def clean_duplicates(content_duplicates, title_duplicates, dry_run=True):
    """Clean up duplicate files, keeping the newest one in each group."""
    if not content_duplicates and not title_duplicates:
        print("No duplicates to clean up.")
        return
    
    print("\nCLEANUP PLAN")
    print("=" * 50)
    
    total_to_delete = 0
    total_space_saved = 0
    
    # Process content duplicates
    for file_hash, files in content_duplicates.items():
        # Sort by modification time (newest first)
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # Keep the newest file, delete the rest
        keep_file = files[0]
        delete_files = files[1:]
        
        print(f"\nContent Hash {file_hash[:12]}...")
        print(f"  KEEP: {os.path.relpath(keep_file, 'scraped_articles')}")
        
        for filepath in delete_files:
            file_size = os.path.getsize(filepath)
            total_to_delete += 1
            total_space_saved += file_size
            
            if dry_run:
                print(f"  DELETE: {os.path.relpath(filepath, 'scraped_articles')} ({file_size} bytes)")
            else:
                try:
                    os.remove(filepath)
                    print(f"  DELETED: {os.path.relpath(filepath, 'scraped_articles')} ({file_size} bytes)")
                except Exception as e:
                    print(f"  ERROR deleting {filepath}: {e}")
    
    # Process title duplicates (be more conservative)
    for title, files in title_duplicates.items():
        if len(files) <= 1:
            continue
            
        # Sort by modification time (newest first)
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # For title duplicates, only delete if they're very similar in size and recent
        keep_file = files[0]
        delete_files = []
        
        keep_size = os.path.getsize(keep_file)
        keep_time = os.path.getmtime(keep_file)
        
        for filepath in files[1:]:
            file_size = os.path.getsize(filepath)
            file_time = os.path.getmtime(filepath)
            
            # Only consider for deletion if size is very similar and file is older
            size_diff = abs(file_size - keep_size) / keep_size
            time_diff = keep_time - file_time
            
            if size_diff < 0.1 and time_diff > 60:  # 10% size diff and 1 minute older
                delete_files.append(filepath)
        
        if delete_files:
            print(f"\nTitle: {title[:60]}{'...' if len(title) > 60 else ''}")
            print(f"  KEEP: {os.path.relpath(keep_file, 'scraped_articles')}")
            
            for filepath in delete_files:
                file_size = os.path.getsize(filepath)
                total_to_delete += 1
                total_space_saved += file_size
                
                if dry_run:
                    print(f"  DELETE: {os.path.relpath(filepath, 'scraped_articles')} ({file_size} bytes)")
                else:
                    try:
                        os.remove(filepath)
                        print(f"  DELETED: {os.path.relpath(filepath, 'scraped_articles')} ({file_size} bytes)")
                    except Exception as e:
                        print(f"  ERROR deleting {filepath}: {e}")
    
    print(f"\nSUMMARY")
    print("=" * 50)
    print(f"Files to delete: {total_to_delete}")
    print(f"Space to save: {total_space_saved / 1024:.1f} KB")
    
    if dry_run:
        print("\nThis was a DRY RUN - no files were actually deleted.")
        print("Run with --execute to actually delete the files.")
    else:
        print(f"\nCleanup completed! Deleted {total_to_delete} duplicate files.")


def main():
    """Main function."""
    import sys
    
    dry_run = "--execute" not in sys.argv
    
    if dry_run:
        print("DUPLICATE CLEANUP (DRY RUN)")
        print("=" * 50)
        print("This will show what would be deleted without actually deleting files.")
        print("Add --execute to actually perform the cleanup.")
        print()
    else:
        print("DUPLICATE CLEANUP (EXECUTING)")
        print("=" * 50)
        print("This will actually delete duplicate files!")
        print()
    
    # Find duplicates
    content_duplicates, title_duplicates = find_duplicates()
    
    if content_duplicates or title_duplicates:
        # Clean up duplicates
        clean_duplicates(content_duplicates, title_duplicates, dry_run)
    else:
        print("No duplicates found - your articles are already clean!")


if __name__ == "__main__":
    main()
