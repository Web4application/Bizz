import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Sparkles } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-tr from-[#111827] via-[#1f2937] to-[#111827] text-white p-6 flex flex-col items-center justify-center">
      <Card className="max-w-md w-full bg-[#1f2937] border-none shadow-2xl">
        <CardContent className="p-6">
          <h1 className="text-4xl font-bold mb-4 text-center">Welcome to Bizz</h1>
          <p className="mb-6 text-center text-gray-300">
            Your modern business automation toolkit. Connect services, analyze data, and deploy seamlessly.
          </p>
          <div className="flex justify-center">
            <Button className="gap-2 px-6 py-2 text-lg">
              <Sparkles className="w-5 h-5" /> Get Started
            </Button>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
