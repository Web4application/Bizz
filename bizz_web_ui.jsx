import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Sparkles, BarChart2, FileText, Settings } from "lucide-react";
import { motion } from "framer-motion";

export default function Home() {
  const handleStart = () => {
    fetch("/api/assistant/start")
      .then(res => res.json())
      .then(data => alert("AI Assistant: " + data.message))
      .catch(err => console.error("Assistant failed:", err));
  };

  return (
    <main className="min-h-screen bg-gradient-to-tr from-[#111827] via-[#1f2937] to-[#111827] text-white p-6 flex flex-col items-center justify-center overflow-hidden">
      <motion.div
        className="absolute w-full h-full bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-indigo-900/10 to-transparent animate-pulse"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.5 }}
      />

      <Card className="max-w-2xl w-full bg-[#1f2937] border-none shadow-2xl relative z-10">
        <CardContent className="p-8">
          <h1 className="text-4xl font-bold mb-6 text-center">Welcome to Bizz</h1>
          <p className="mb-8 text-center text-gray-300">
            Your modern business automation toolkit. Connect services, analyze data, and deploy seamlessly.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6">
            <Card className="bg-[#111827] p-4 flex flex-col items-center text-center hover:ring hover:ring-indigo-500 transition">
              <BarChart2 className="w-8 h-8 text-indigo-400 mb-2" />
              <p className="font-semibold">Analytics Dashboard</p>
              <p className="text-sm text-gray-400">Visualize key business metrics.</p>
            </Card>
            <Card className="bg-[#111827] p-4 flex flex-col items-center text-center hover:ring hover:ring-yellow-400 transition">
              <FileText className="w-8 h-8 text-yellow-400 mb-2" />
              <p className="font-semibold">Data Upload</p>
              <p className="text-sm text-gray-400">Ingest CSV, JSON or API feeds.</p>
            </Card>
            <Card className="bg-[#111827] p-4 flex flex-col items-center text-center hover:ring hover:ring-pink-400 transition">
              <Settings className="w-8 h-8 text-pink-400 mb-2" />
              <p className="font-semibold">Automation Rules</p>
              <p className="text-sm text-gray-400">Trigger actions based on input changes.</p>
            </Card>
            <Card className="bg-[#111827] p-4 flex flex-col items-center text-center hover:ring hover:ring-green-400 transition">
              <Sparkles className="w-8 h-8 text-green-400 mb-2" />
              <p className="font-semibold">Deploy</p>
              <p className="text-sm text-gray-400">Push to cloud or run locally in Docker.</p>
            </Card>
          </div>

          <div className="flex justify-center">
            <Button className="gap-2 px-6 py-2 text-lg" onClick={handleStart}>
              <Sparkles className="w-5 h-5" /> Launch AI Assistant
            </Button>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
