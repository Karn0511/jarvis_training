import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion";
import { Select, SelectTrigger, SelectContent, SelectItem } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Tooltip, TooltipProvider, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";

const Settings = () => {
    const [modelQuality, setModelQuality] = useState('balanced');
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
                <p className="text-muted-foreground">Manage your preferences.</p>
            </div>
            <Accordion type="single" collapsible className="space-y-4">
                <AccordionItem value="general">
                    <AccordionTrigger>General</AccordionTrigger>
                    <AccordionContent>
                        <Card>
                            <CardContent className="space-y-6 pt-6">
                                <div className="flex items-center justify-between">
                                    <div className="space-y-0.5">
                                        <Label>Dark Mode</Label>
                                        <p className="text-sm text-muted-foreground">Enable dark theme</p>
                                    </div>
                                    <Switch defaultChecked />
                                </div>
                                <div className="flex items-center justify-between">
                                    <div className="space-y-0.5">
                                        <Label>Notifications</Label>
                                        <p className="text-sm text-muted-foreground">Receive alerts</p>
                                    </div>
                                    <Switch />
                                </div>
                            </CardContent>
                        </Card>
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="ai">
                    <AccordionTrigger>AI Configuration</AccordionTrigger>
                    <AccordionContent>
                        <Card>
                            <CardContent className="space-y-6 pt-6">
                                <div className="space-y-2">
                                    <Label>Local Mode</Label>
                                    <Checkbox defaultChecked /> <span className="text-xs text-muted-foreground ml-2">Force local model only</span>
                                </div>
                                <div className="space-y-2">
                                    <Label>Quality vs Speed</Label>
                                    <Select onValueChange={setModelQuality}>
                                        <SelectTrigger>{modelQuality}</SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="fast">fast</SelectItem>
                                            <SelectItem value="balanced">balanced</SelectItem>
                                            <SelectItem value="thorough">thorough</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                                <TooltipProvider>
                                    <Tooltip>
                                        <TooltipTrigger asChild>
                                            <Button variant="outline">What is this?</Button>
                                        </TooltipTrigger>
                                        <TooltipContent>Adjust heuristic guidance for responses.</TooltipContent>
                                    </Tooltip>
                                </TooltipProvider>
                            </CardContent>
                        </Card>
                    </AccordionContent>
                </AccordionItem>
            </Accordion>
            <div className="flex justify-end">
                <Button>Save Changes</Button>
            </div>
        </div>
    );
};

export default Settings;
