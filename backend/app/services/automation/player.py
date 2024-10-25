from playwright.async_api import async_playwright, Browser, Page
from typing import List, Dict, Any, Optional
import json
import os
import asyncio
from datetime import datetime

class AutomationService:
    def __init__(self, user_data_dir: str):
        self.user_data_dir = user_data_dir
        self.recording: List[Dict[str, Any]] = []
        self.is_recording = False
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None

    async def start_browser(self) -> None:
        """Start browser with persistent context for Telegram session."""
        playwright = await async_playwright().start()
        self._browser = await playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=False,  # Set to True for production headless mode
            viewport={'width': 1280, 'height': 720}
        )
        self._page = await self._browser.new_page()

    async def start_recording(self) -> None:
        """Start recording user interactions."""
        if not self._page:
            raise RuntimeError("Browser not started")
        
        self.recording = []
        self.is_recording = True
        
        # Setup event listeners
        async def handle_click(event):
            if not self.is_recording:
                return
            
            element = await self._page.evaluate('element => {
                return {
                    selector: element.id || element.className,
                    innerText: element.innerText,
                    tag: element.tagName.toLowerCase()
                }
            }', event)
            
            self.recording.append({
                'type': 'click',
                'timestamp': datetime.now().isoformat(),
                'x': event['x'],
                'y': event['y'],
                'element': element,
                'url': self._page.url
            })

        async def handle_navigation(response):
            if not self.is_recording:
                return
            
            self.recording.append({
                'type': 'navigation',
                'timestamp': datetime.now().isoformat(),
                'url': response.url,
                'status': response.status
            })

        # Register event listeners
        await self._page.evaluate('''
            window.addEventListener('click', event => {
                window.__recordClick(event);
            });
        ''')
        
        self._page.on('click', handle_click)
        self._page.on('response', handle_navigation)

    async def stop_recording(self) -> List[Dict[str, Any]]:
        """Stop recording and return the recorded steps."""
        self.is_recording = False
        return self.recording

    async def verify_routine(self, routine: List[Dict[str, Any]]) -> bool:
        """Verify a recorded routine can be played back."""
        try:
            await self.playback_routine(routine, verify_mode=True)
            return True
        except Exception as e:
            print(f"Verification failed: {str(e)}")
            return False

    async def playback_routine(self, routine: List[Dict[str, Any]], verify_mode: bool = False) -> None:
        """Play back a recorded routine."""
        if not self._page:
            raise RuntimeError("Browser not started")

        for step in routine:
            try:
                if step['type'] == 'click':
                    # Wait for navigation or network idle if this is a critical click
                    await self._page.wait_for_load_state('networkidle')
                    
                    # Try to find element by multiple strategies
                    element = None
                    if 'element' in step:
                        try:
                            # Try by ID
                            if step['element'].get('selector'):
                                element = await self._page.wait_for_selector(
                                    f"#{step['element']['selector']}", 
                                    timeout=5000
                                )
                            # Try by text content
                            if not element and step['element'].get('innerText'):
                                element = await self._page.wait_for_selector(
                                    f"text={step['element']['innerText']}", 
                                    timeout=5000
                                )
                        except:
                            pass

                    # Fallback to coordinates if element not found
                    if element:
                        await element.click()
                    else:
                        await self._page.mouse.click(step['x'], step['y'])
                    
                    # Add wait time after click (configurable)
                    await asyncio.sleep(1)

                elif step['type'] == 'navigation':
                    await self._page.wait_for_load_state('networkidle')
                    
                    # If URL doesn't match, try to navigate
                    if self._page.url != step['url']:
                        await self._page.goto(step['url'])

                # Handle special cases like waiting for video
                if 'wait_time' in step:
                    await asyncio.sleep(step['wait_time'])

            except Exception as e:
                if verify_mode:
                    raise
                print(f"Error during playback: {str(e)}")
                # Implement retry logic here if needed

    async def close(self) -> None:
        """Close the browser and cleanup."""
        if self._browser:
            await self._browser.close()
            self._browser = None
            self._page = None

# TO-DO: Implement automation service