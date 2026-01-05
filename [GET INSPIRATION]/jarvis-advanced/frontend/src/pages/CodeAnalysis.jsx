import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Play, Loader2 } from "lucide-react";

const CodeAnalysis = () => {
    const [code, setCode] = useState('');
    const [analyzing, setAnalyzing] = useState(false);
    const [result, setResult] = useState(null);

    const handleAnalyze = () => {
        if (!code.trim()) return;

        setAnalyzing(true);
        // Simulate analysis
        setTimeout(() => {
            setResult({
                quality: 8.5,
                issues: 2,
                suggestions: [
                    "Consider using list comprehension for better performance",
                    "Add type hints for better maintainability"
                ]
            });
            setAnalyzing(false);
        }, 2000);
    };

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Code Analysis</h2>
                <p className="text-muted-foreground">Analyze and optimize your code.</p>
            </div>

            <div className="grid gap-6 lg:grid-cols-2">
                <Card className="h-full">
                    <CardHeader>
                        <CardTitle>Input Code</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <Textarea
                            value={code}
                            onChange={(e) => setCode(e.target.value)}
                            placeholder="Paste your code here..."
                            className="min-h-[400px] font-mono"
                        />
                        <Button
                            onClick={handleAnalyze}
                            disabled={analyzing || !code.trim()}
                            className="w-full"
                        >
                            {analyzing ? (
                                <>
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                    Analyzing...
                                </>
                            ) : (
                                <>
                                    <Play className="mr-2 h-4 w-4" />
                                    Analyze Code
                                </>
                            )}
                        </Button>
                    </CardContent>
                </Card>

                <Card className="h-full">
                    <CardHeader>
                        <CardTitle>Analysis Results</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {result ? (
                            <div className="space-y-6">
                                <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
                                    <span className="font-medium">Quality Score</span>
                                    <span className="text-2xl font-bold text-green-500">{result.quality}/10</span>
                                </div>

                                <div>
                                    <h4 className="font-medium mb-2">Suggestions</h4>
                                    <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground">
                                        {result.suggestions.map((s, i) => (
                                            <li key={i}>{s}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        ) : (
                            <div className="h-[400px] flex items-center justify-center text-muted-foreground">
                                Run analysis to see results
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default CodeAnalysis;
