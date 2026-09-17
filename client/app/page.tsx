"use client";

import VideoPlaceholder from "@/components/VideoPlaceholder";
import { useEffect, useRef, useState } from "react";

export default function Home() {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const previousURL = useRef<string | null>(null);

  useEffect(() => {
    const inputRef = previousURL.current;
    return () => {
      if (inputRef) {
        URL.revokeObjectURL(inputRef);
        previousURL.current = null;
      }
    };
  }, []);

  const openFilePicker = () => inputRef.current?.click();

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;

    if (previousURL.current) {
      URL.revokeObjectURL(previousURL.current);
    }

    const url = URL.createObjectURL(file);
    previousURL.current = url;
    setVideoUrl(url);
    setFileName(file.name);
  };

  const onRemove = () => {
    if (previousURL.current) {
      URL.revokeObjectURL(previousURL.current);
    }

    setVideoUrl(null);
    setFileName(null);

    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="w-full max-w-4xl text-center">
        <header className="mb-8">
          <h1 className="text-4xl font-bold">Video Subtitler</h1>
          <p className="text-gray-600 mt-2">
            Translate and generate subtitles for your videos. Start by uploading
            a video or select an example.
          </p>
        </header>

        {videoUrl ? (
          <VideoPlaceholder
            fileName={fileName}
            videoUrl={videoUrl}
            handleRemove={onRemove}
          />
        ) : (
          <section className="border-white-500 border-dashed border-2 shadow rounded-lg p-6 text-center aspect-video flex flex-col justify-center">
            <h2 className="text-xl font-semibold mb-4">Get started</h2>
            <p className="text-gray-500 mb-4">
              Upload a video file to generate subtitles and translations.
            </p>

            <div className="flex gap-4 justify-center">
              <button
                onClick={openFilePicker}
                className="px-4 py-2 bg-blue-600 text-white rounded"
              >
                Upload Video
              </button>
            </div>
          </section>
        )}

        <input
          ref={inputRef}
          type="file"
          accept="video/*"
          onChange={onFileChange}
          className="hidden"
          aria-hidden
        />
      </div>
    </main>
  );
}
