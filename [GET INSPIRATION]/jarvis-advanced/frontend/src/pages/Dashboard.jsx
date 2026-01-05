import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Activity, Code2, MessageSquare, Zap } from "lucide-react";
import { Link } from 'react-router-dom';

const Dashboard = () => {
    const stats = [
        { title: "Active Chats", value: "3", icon: MessageSquare, color: "text-blue-500" },
        { title: "Code Analyses", value: "12", icon: Code2, color: "text-purple-500" },
        { title: "System Status", value: "Online", icon: Activity, color: "text-green-500" },
        { title: "AI Model", value: "GPT-4", icon: Zap, color: "text-yellow-500" },
    ];

    return (
        <div className="space-y-8">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
                <p className="text-muted-foreground">Welcome back to Jarvis AI.</p>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {stats.map((stat, index) => {
                    const Icon = stat.icon;
                    return (
                        <Card key={index}>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">
                                    {stat.title}
                                </CardTitle>
                                <Icon className={`h-4 w-4 ${stat.color}`} />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">{stat.value}</div>
                            </CardContent>
                        </Card>
                    );
                })}
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-4">
                    <CardHeader>
                        <CardTitle>Recent Activity</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {[1, 2, 3].map((i) => (
                                <div key={i} className="flex items-center">
                                    <div className="ml-4 space-y-1">
                                        <p className="text-sm font-medium leading-none">Code Analysis #{i}</p>
                                        <p className="text-sm text-muted-foreground">
                                            Analyzed python script for optimization
                                        </p>
                                    </div>
                                    <div className="ml-auto font-medium">Just now</div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                <Card className="col-span-3">
                    <CardHeader>
                        <CardTitle>Quick Actions</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <Link to="/chat">
                            <Button className="w-full justify-start" variant="outline">
                                <MessageSquare className="mr-2 h-4 w-4" />
                                New Chat
                            </Button>
                        </Link>
                        <Link to="/analyze">
                            <Button className="w-full justify-start" variant="outline">
                                <Code2 className="mr-2 h-4 w-4" />
                                Analyze Code
                            </Button>
                        </Link>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default Dashboard;
