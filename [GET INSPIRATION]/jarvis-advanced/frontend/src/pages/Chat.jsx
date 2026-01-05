import React, { useState } from 'react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send } from "lucide-react";

const Chat = () => {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I am Jarvis. How can I help you today?' }
    ]);
    const [input, setInput] = useState('');

    const handleSend = () => {
        if (!input.trim()) return;

        setMessages(prev => [...prev, { role: 'user', content: input }]);
        setInput('');

        // Simulate response
        setTimeout(() => {
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'I am a demo version. Connect to backend for real responses.'
            }]);
        }, 1000);
    };

    return (
        <div className="h-[calc(100vh-8rem)] flex flex-col space-y-4">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Chat</h2>
                <p className="text-muted-foreground">Interact with Jarvis AI.</p>
            </div>

            <Card className="flex-1 flex flex-col p-4 overflow-hidden">
                <div className="flex-1 overflow-y-auto space-y-4 mb-4">
                    {messages.map((msg, i) => (
                        <div
                            key={i}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[80%] rounded-lg p-3 ${msg.role === 'user'
                                        ? 'bg-primary text-primary-foreground'
                                        : 'bg-muted'
                                    }`}
                            >
                                {msg.content}
                            </div>
                        </div>
                    ))}
                </div>

                <div className="flex gap-2">
                    <Input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Type a message..."
                        className="flex-1"
                    />
                    <Button onClick={handleSend}>
                        <Send className="h-4 w-4" />
                    </Button>
                </div>
            </Card>
        </div>
    );
};

export default Chat;
