"use client";

import VideoPlaceholder from "@/components/VideoPlaceholder";
import { useEffect, useRef, useState } from "react";

export default function Home() {
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>("");
  const inputRef = useRef<HTMLInputElement | null>(null);
  const previousURL = useRef<string | null>(null);

  useEffect(() => {
    return () => {
      if (previousURL.current) {
        URL.revokeObjectURL(previousURL.current);
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
    setVideoFile(file);
    setPreviewUrl(url);
  };

  const onRemove = () => {
    if (previousURL.current) {
      URL.revokeObjectURL(previousURL.current);
      previousURL.current = null;
    }

    setVideoFile(null);
    setPreviewUrl("");

    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,#1e293b_0%,#0f172a_38%,#020617_100%)] px-4 py-8 text-slate-50 sm:px-6 lg:px-8">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-8">
        <div className="flex flex-col items-center my-10">
          <div className="max-w-2xl flex flex-col items-center text-center">
            <h1 className="mt-4 text-4xl font-black tracking-tight text-white sm:text-5xl">
              Turn raw video into polished subtitles.
            </h1>
            <p className="mt-4 max-w-xl text-sm text-slate-300 sm:text-base">
              Upload a video, choose a language, and let Vidora transcribe,
              translate, and export a clean subtitle-ready result.
            </p>
          </div>
        </div>

        {videoFile ? (
          <VideoPlaceholder
            videoFile={videoFile}
            preview={previewUrl}
            setPreview={setPreviewUrl}
            handleRemove={onRemove}
          />
        ) : (
          <section className="relative overflow-hidden mx-auto rounded-[28px] border border-dashed border-cyan-400/40 bg-slate-950/40 p-6 shadow-2xl shadow-slate-950/30 backdrop-blur-sm sm:p-18">
            <div className="relative mx-auto flex max-w-3xl flex-col items-center justify-center gap-8 text-center">
              <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-cyan-500/15 ring-1 ring-cyan-400/40">
                <svg
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                  className="h-10 w-10 text-cyan-300"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.8"
                >
                  <path d="M15 10.5V7.8A1.8 1.8 0 0 0 13.2 6H6.8A1.8 1.8 0 0 0 5 7.8v8.4A1.8 1.8 0 0 0 6.8 18h6.4A1.8 1.8 0 0 0 15 16.2v-2.7l5 3.3V7.2l-5 3.3Z" />
                </svg>
              </div>

              <div>
                <h2 className="text-2xl font-bold text-white sm:text-3xl">
                  Ready to subtitle your next video?
                </h2>
                <p className="mt-3 text-sm text-slate-300 sm:text-base">
                  Drag your file in or upload it below to generate subtitles and
                  translations in minutes.
                </p>
              </div>

              <button
                onClick={openFilePicker}
                className="inline-flex items-center justify-center rounded-xl bg-cyan-400 px-6 py-3 text-base font-semibold text-slate-950 shadow-lg shadow-cyan-500/30 transition-transform hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-cyan-300 focus:ring-offset-2 focus:ring-offset-slate-950"
              >
                Upload video
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
