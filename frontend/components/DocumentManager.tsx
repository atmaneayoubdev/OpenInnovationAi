"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Trash2, Download } from "lucide-react";

interface Document {
  filename: string;
  extension: string;
}

export function DocumentManager() {
  const [file, setFile] = useState<File | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const fetchDocuments = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/v1/documents");
      if (!response.ok) {
        throw new Error("Failed to fetch documents");
      }
      const data = await response.json();
      setDocuments(data.documents);
    } catch (error) {
      console.error("Error fetching documents:", error);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        "http://localhost:8000/api/v1/document-upload",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      await fetchDocuments();
      setFile(null);
    } catch (error) {
      console.error("Error uploading file:", error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async (filename: string) => {
    setIsDeleting(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/delete-pdf", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ filename }),
      });

      if (!response.ok) {
        throw new Error("Delete failed");
      }

      await fetchDocuments();
    } catch (error) {
      console.error("Error deleting file:", error);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleClearAll = async () => {
    setIsDeleting(true);
    try {
      await Promise.all(
        documents.map((doc) =>
          fetch("http://127.0.0.1:8000/api/v1/delete-pdf", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ filename: doc.filename }),
          })
        )
      );
      await fetchDocuments();
    } catch (error) {
      console.error("Error clearing all documents:", error);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleDownload = (filename: string) => {
    window.open(`http://127.0.0.1:8000/documents/${filename}`, "_blank");
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Document Manager</CardTitle>
        <CardDescription>Upload and manage your documents</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid w-full items-center gap-4">
          <div className="flex flex-col space-y-1.5">
            <Label htmlFor="file">Upload Document</Label>
            <Input id="file" type="file" onChange={handleFileChange} />
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button onClick={handleUpload} disabled={!file || isUploading}>
          {isUploading ? "Uploading..." : "Upload"}
        </Button>
      </CardFooter>
      <CardContent>
        <h3 className="text-lg font-semibold mb-2">Current Documents</h3>
        {documents.length > 0 ? (
          <ul className="space-y-2">
            {documents.map((doc, index) => (
              <li key={index} className="flex items-center justify-between">
                <span className="truncate max-w-[200px]" title={doc.filename}>
                  {doc.filename}
                </span>
                <div className="flex space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleDownload(doc.filename)}
                  >
                    <Download className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => handleDelete(doc.filename)}
                    disabled={isDeleting}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>No documents uploaded yet.</p>
        )}
      </CardContent>
      <CardFooter>
        <Button
          variant="destructive"
          onClick={handleClearAll}
          disabled={documents.length === 0 || isDeleting}
          className="w-full"
        >
          Clear All Documents
        </Button>
      </CardFooter>
    </Card>
  );
}
