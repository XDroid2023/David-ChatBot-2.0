import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime
import threading
import subprocess
import queue

class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        # Extract colors from kwargs or use defaults
        self.normal_bg = kwargs.pop('bg', '#2196F3')
        self.hover_bg = kwargs.pop('activebackground', '#1976D2')
        
        super().__init__(master, **kwargs)
        self.configure(
            relief='flat',
            bg=self.normal_bg,
            fg='white',
            activebackground=self.hover_bg,
            activeforeground='white',
            font=('Helvetica', 11, 'bold'),
            padx=15,
            pady=8,
            cursor='hand2',
            borderwidth=0,
            highlightthickness=0
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, event):
        self.configure(bg=self.hover_bg)

    def on_leave(self, event):
        self.configure(bg=self.normal_bg)

class ModernEntry(ttk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            font=('Helvetica', 10),
        )

class DavidChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("David's Chatbot")
        self.root.geometry("500x600")
        self.root.configure(bg='#2e2e2e')
        
        # TTS state
        self.tts_queue = queue.Queue()
        self.speaking_thread = None
        
        # Add cleanup handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # DJs information
        self.djs = {
            "DJ MICKY": {
                "style": "House and Deep Tech",
                "specialty": "Groovy basslines and infectious rhythms",
                "events": ["Club Night", "Beach Party"]
            },
            "DJ IPRO": {
                "style": "Techno and Progressive",
                "specialty": "Mind-bending drops and epic buildups",
                "events": ["Warehouse Rave", "Club Night"]
            },
            "DJ FUSION": {
                "style": "Tropical House and Chill",
                "specialty": "Smooth transitions and summer vibes",
                "events": ["Beach Party", "Sunday Brunch"]
            }
        }
        
        # Events information
        self.events = {
            "Club Night": {
                "date": "Every Friday",
                "time": "10 PM - 3 AM",
                "location": "The Underground Club",
                "description": "Deep house and techno night featuring DJ MICKY and DJ IPRO"
            },
            "Beach Party": {
                "date": "Every Saturday",
                "time": "4 PM - 10 PM",
                "location": "Sunset Beach",
                "description": "Sunset sessions with DJ FUSION and DJ MICKY"
            },
            "Warehouse Rave": {
                "date": "Last Saturday of month",
                "time": "11 PM - 6 AM",
                "location": "The Factory",
                "description": "Hard techno and industrial beats with DJ IPRO"
            },
            "Sunday Brunch": {
                "date": "Every Sunday",
                "time": "12 PM - 5 PM",
                "location": "Sky Lounge",
                "description": "Relaxed vibes with DJ FUSION"
            }
        }
        
        # Website information
        self.website_info = {
            "url": "www.davidchatbot.com",
            "features": [
                "Event Calendar & Tickets",
                "DJ Profiles & Music",
                "Photo Gallery",
                "VIP Reservations"
            ],
            "social_media": {
                "Instagram": "@davidchatbot",
                "Facebook": "DavidChatbotOfficial",
                "Twitter": "@davidchatbot"
            },
            "description": "Your one-stop destination for the best electronic music events!"
        }
        
        self.setup_gui()
        self.initialize_chat()
        self.process_tts_queue()  # Start TTS queue processing
    
    def process_tts_queue(self):
        """Process TTS queue periodically"""
        if not self.tts_queue.empty() and (self.speaking_thread is None or not self.speaking_thread.is_alive()):
            text = self.tts_queue.get_nowait()
            self.speaking_thread = threading.Thread(target=self.speak, args=(text,))
            self.speaking_thread.daemon = True
            self.speaking_thread.start()
        
        # Schedule next check
        self.root.after(100, self.process_tts_queue)

    def speak(self, text):
        """Speak text using macOS say command"""
        try:
            # Clean the text
            cleaned_text = text.replace('"', '').replace("'", "")
            # Use subprocess.run to ensure the command completes before continuing
            subprocess.run(['say', cleaned_text], check=True)
        except Exception as e:
            print(f"TTS Error: {e}")

    def setup_gui(self):
        """Set up the GUI components"""
        # Configure styles
        style = ttk.Style()
        style.configure('Header.TLabel',
                       font=('Helvetica', 14),
                       foreground='white',
                       background='#2e2e2e')
        
        style.configure('Content.TFrame',
                       background='#2e2e2e')
        
        # Create header
        header_frame = ttk.Frame(self.root, style='Content.TFrame')
        header_frame.pack(fill='x', padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(header_frame,
                              text="David's Chatbot",
                              style='Header.TLabel')
        title_label.pack(side='left')
        
        # Main content
        main_frame = ttk.Frame(self.root, style='Content.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Chat display
        self.chat_display = tk.Text(
            main_frame,
            wrap=tk.WORD,
            font=('Helvetica', 10),
            bg='#3e3e3e',
            fg='white',
            insertbackground='white',
            selectbackground='#555555',
            relief='flat',
            padx=8,
            pady=8,
            height=20
        )
        self.chat_display.pack(fill='both', expand=True, pady=(0,10))
        self.chat_display.configure(state='disabled')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.chat_display.yview)
        scrollbar.pack(side='right', fill='y')
        self.chat_display['yscrollcommand'] = scrollbar.set
        
        # Input frame
        input_frame = ttk.Frame(main_frame, style='Content.TFrame')
        input_frame.pack(fill='x', pady=(5,0))
        
        # Input field
        self.user_input = ModernEntry(input_frame)
        self.user_input.pack(side='left', fill='x', expand=True, padx=(0,5))
        
        # Send button with explicit colors
        self.send_button = ModernButton(
            input_frame,
            text="Send",
            bg='#2196F3',  # Material Design Blue
            fg='white',
            activebackground='#1976D2',  # Darker blue on hover
            activeforeground='white',
            command=self.process_input
        )
        self.send_button.pack(side='right')
        
        # Bind Enter key
        self.user_input.bind('<Return>', lambda e: self.process_input())
        
        # Start datetime updates
        # self.update_datetime()
    
    def initialize_chat(self):
        """Initialize chat state and start conversation"""
        self.state = "NAME"
        self.name = None
        self.age = None
        self.favorite_dj = None
        self.favorite_song = None
        self.feedback = None
        
        self.add_message("Hi! I'm David, your friendly music & events chatbot! \nWhat's your name?")
    
    def update_datetime(self):
        """Update the date and time display"""
        current_time = datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
        # self.datetime_label.config(text=current_time)
        self.root.after(1000, self.update_datetime)
    
    def add_message(self, message):
        """Add a message to the chat display"""
        self.chat_display.configure(state='normal')
        
        # Get current timestamp in 24-hour format
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format the message with timestamp
        if message.startswith("You: "):
            formatted_message = f"\n[{current_time}] {message}\n"
        else:
            formatted_message = f"\n[{current_time}] David: {message}\n"
            # Queue the bot's message for speech
            self.tts_queue.put(message)
        
        self.chat_display.insert(tk.END, formatted_message)
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def process_input(self):
        user_input = self.user_input.get().strip()
        if not user_input:
            return
        
        # Clear input field
        self.user_input.delete(0, tk.END)
        
        # Add user's message to chat
        self.add_message("You: " + user_input)
        
        # Process based on current state
        if self.state == "NAME":
            self.name = user_input
            self.state = "AGE"
            response = f"Nice to meet you, {self.name}! How old are you?"
            self.add_message(response)
            
        elif self.state == "AGE":
            try:
                self.age = int(user_input)
                if self.age < 18:
                    response = "Sorry, you must be 18 or older to use this chatbot. The application will close in 5 seconds."
                    self.add_message(response)
                    self.user_input.configure(state='disabled')
                    self.send_button.configure(state='disabled')
                    # Schedule application closure after 5 seconds
                    self.root.after(5000, self.close_app)
                    return
                
                self.state = "SONG"
                response = "What kind of music do you like?"
                self.add_message(response)
                
            except ValueError:
                self.add_message("Please enter a valid number for your age.")
                
        elif self.state == "SONG":
            music_preference = user_input.lower()
            if "house" in music_preference or "tech" in music_preference:
                response = f"Great choice! I recommend checking out DJ MICKY's house and deep tech sets. They're known for groovy basslines!"
            elif "chill" in music_preference or "tropical" in music_preference:
                response = f"Perfect! DJ FUSION's tropical house sets would be perfect for you. Very relaxing vibes!"
            elif "techno" in music_preference or "progressive" in music_preference:
                response = f"Awesome! You should definitely check out DJ IPRO's techno sets at The Factory. Mind-bending beats guaranteed!"
            else:
                response = f"Cool! Based on that, I think you'd enjoy our Sunday Brunch sessions with DJ FUSION. It's a great mix of different styles!"
            self.add_message(response)
            self.state = "DJS"
            dj_message = "\nLet me introduce you to our amazing resident DJs:\n\n"
            for dj_name, details in self.djs.items():
                dj_message += f" {dj_name}\n"
                dj_message += f"   • Style: {details['style']}\n"
                dj_message += f"   • Known for: {details['specialty']}\n"
                dj_message += f"   • Plays at: {', '.join(details['events'])}\n\n"
            self.add_message(dj_message)
                
            # Ask about events with a slight delay to allow DJ info to be read
            self.root.after(1000, lambda: self.add_message(
                "Would you like to hear about our upcoming events and gigs? Please say yes or no."
            ))
            
        elif self.state == "DJS":
            if user_input.lower() in ['yes', 'y', 'yeah', 'sure']:
                events_message = "\nHere are our regular events:\n\n"
                for event_name, details in self.events.items():
                    events_message += f" {event_name}\n"
                    events_message += f"   • When: {details['date']}, {details['time']}\n"
                    events_message += f"   • Where: {details['location']}\n"
                    events_message += f"   • What: {details['description']}\n\n"
                self.add_message(events_message)
                
                # Ask about favorite DJ with a slight delay
                self.root.after(1000, lambda: self.add_message(
                    "Which of our resident DJs is your favorite? Please choose DJ MICKY, DJ IPRO, or DJ FUSION."
                ))
                self.state = "FAVORITE_DJ"
            else:
                self.add_message("No problem! Which of our resident DJs is your favorite? Please choose DJ MICKY, DJ IPRO, or DJ FUSION.")
                self.state = "FAVORITE_DJ"
            
        elif self.state == "FAVORITE_DJ":
            self.favorite_dj = user_input.upper()
            if self.favorite_dj in self.djs:
                dj_info = self.djs[self.favorite_dj]
                response = f"Great choice! {self.favorite_dj} is amazing at {dj_info['style']}!\n"
                response += f"You can catch them at: {', '.join(dj_info['events'])}"
                self.add_message(response)
            self.state = "FEEDBACK"
            self.add_message("How was your experience chatting with me today? Please rate from 1 to 5 stars, where 5 is the best!")
            
        elif self.state == "FEEDBACK":
            try:
                feedback_rating = int(user_input)
                if 1 <= feedback_rating <= 5:
                    self.feedback = feedback_rating
                    self.state = "WEBSITE"
                    
                    # Final response
                    response = f"\nThank you for chatting with me, {self.name}! Here's a summary of our conversation:\n"
                    response += f"• Age: {self.age}\n"
                    response += f"• Favorite DJ: {self.favorite_dj}\n"
                    response += f"• Your Feedback: {'⭐' * self.feedback}\n\n"
                    response += "I'd love to see you at our events!\n"
                    self.add_message(response)
                    
                    # Website information with slight delay
                    self.root.after(1000, lambda: self.add_message(
                        f"\nBefore you go, check out our website at {self.website_info['url']}!\n\n"
                        f"{self.website_info['description']}\n\n"
                        "Features:\n" +
                        "\n".join(f"• {feature}" for feature in self.website_info['features']) +
                        "\n\nFollow us on social media:\n" +
                        "\n".join(f"• {platform}: {handle}" for platform, handle in self.website_info['social_media'].items()) +
                        "\n\nHave a great day! Hope to see you at our next event! 🎉"
                    ))
                    
                    # Disable input after conversation is done
                    self.user_input.configure(state='disabled')
                    self.send_button.configure(state='disabled')
                else:
                    self.add_message("Please rate between 1 and 5 stars.")
            except ValueError:
                self.add_message("Please enter a valid rating between 1 and 5 stars.")

    def close_app(self):
        """Close the application"""
        self.root.destroy()

    def on_closing(self):
        """Clean up resources before closing"""
        try:
            subprocess.run(['pkill', 'say'], capture_output=True)
        except:
            pass
        self.root.destroy()

def main():
    root = tk.Tk()
    app = DavidChatbot(root)
    root.mainloop()

if __name__ == "__main__":
    main()
