"use client";

import { useState, useEffect } from "react";
import { DocumentManager } from "../components/DocumentManager";
import { ChatInterface } from "../components/ChatInterface";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { RefreshCw } from "lucide-react";

export default function Home() {
  const [healthStatus, setHealthStatus] = useState<string>("Checking...");

  const checkHealth = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/health-check");
      if (response.ok) {
        setHealthStatus("Healthy");
      } else {
        setHealthStatus("Unhealthy");
      }
    } catch {
      setHealthStatus("Error");
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">
            OpenInnovationAI Dashboard
          </h1>
          <p className="text-sm text-gray-600">Created by Atmane Ayoub</p>
        </div>
        <Card className="mb-6">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-xl font-semibold">
              System Status
            </CardTitle>
            <Button variant="outline" size="icon" onClick={checkHealth}>
              <RefreshCw className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent>
            <p
              className={`text-lg font-semibold ${
                healthStatus === "Healthy" ? "text-green-600" : "text-red-600"
              }`}
            >
              {healthStatus}
            </p>
          </CardContent>
        </Card>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Document Manager</CardTitle>
            </CardHeader>
            <CardContent>
              <DocumentManager />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Chat Interface</CardTitle>
            </CardHeader>
            <CardContent>
              <ChatInterface />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
