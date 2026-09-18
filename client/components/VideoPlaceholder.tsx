import axios from "axios";
import { Dispatch, SetStateAction, useState } from "react";

interface VideoPlaceholderProps {
  videoFile: File;
  preview: string;
  setPreview: Dispatch<SetStateAction<string>>;
  handleRemove: () => void;
}

export default function VideoPlaceholder({
  videoFile,
  preview,
  setPreview,
  handleRemove: onRemove,
}: VideoPlaceholderProps) {
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSuccessful, setIsSuccessful] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState("en");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleProcess = async () => {
    setIsProcessing(true);
    setErrorMessage(null);

    try {
      const formData = new FormData();
      formData.append("video", videoFile);
      formData.append("target_language", selectedLanguage);

      const res = await axios.post(
        "http://127.0.0.1:8000/api/process-video",
        formData,
        { responseType: "blob" },
      );

      const blob = new Blob([res.data], {
        type: (res.headers["content-type"] as string) || "video/mp4",
      });

      if (preview) {
        URL.revokeObjectURL(preview);
      }

      const url = URL.createObjectURL(blob);
      setPreview(url);
      setIsSuccessful(true);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (error: any) {
      setIsSuccessful(false);

      if (error.response) {
        const status = error.response?.status;
        const data = error.response?.data;

        console.error("Response NOT OK. Status:", status);
        console.error("Server Error Data:", data);

        if (status === 422) {
          setErrorMessage(
            "The backend rejected the upload. Check the selected language and file payload.",
          );
        } else {
          setErrorMessage(
            "Your video could not be processed. Please try again.",
          );
        }
      } else if (error.request) {
        setErrorMessage(
          "No response received from the server. Please confirm the backend is running.",
        );
      } else {
        setErrorMessage("Something went wrong while starting the job.");
      }
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <section className="overflow-hidden mx-28 rounded-[28px] border border-white/10 bg-slate-950/70 p-4 shadow-2xl shadow-slate-950/40 backdrop-blur-sm sm:p-6">
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">
            Source file
          </p>
          <p className="mt-1 truncate text-sm font-medium text-slate-200">
            {videoFile.name}
          </p>
        </div>

        <span
          className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold ${
            isSuccessful
              ? "bg-emerald-500/15 text-emerald-300 ring-1 ring-emerald-400/30"
              : isProcessing
                ? "bg-amber-500/15 text-amber-300 ring-1 ring-amber-400/30"
                : "bg-slate-800 text-slate-200 ring-1 ring-white/10"
          }`}
        >
          {isSuccessful
            ? "Ready to download"
            : isProcessing
              ? "Processing"
              : "Ready to process"}
        </span>
      </div>

      <div className="overflow-hidden rounded-2xl border border-white/10 bg-black shadow-inner shadow-slate-900/80">
        <div className="aspect-video bg-slate-900">
          <video
            src={preview}
            controls
            className="h-full w-full object-cover"
          />
        </div>
      </div>

      {isProcessing && (
        <div className="mt-4 rounded-xl border border-amber-400/20 bg-amber-500/10 px-4 py-3 text-sm text-amber-100">
          Processing your video and generating subtitle tracks...
        </div>
      )}

      {errorMessage && (
        <div className="mt-4 rounded-xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-100">
          {errorMessage}
        </div>
      )}

      <div className="mt-5 flex flex-col gap-4 rounded-2xl border border-white/10 bg-slate-900/60 p-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="w-full sm:max-w-xs">
          <label
            htmlFor="language-select"
            className="mb-2 pl-2 block text-xs font-medium uppercase tracking-[0.2em] text-slate-300"
          >
            Source language
          </label>
          <select
            id="language-select"
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="rounded-xl border border-white/10 bg-slate-950 px-3 py-2.5 text-sm text-slate-100 outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-500/30"
            aria-label="Select target language"
          >
            <option value="en">English</option>
            <option value="es">Spanish</option>
            <option value="tl">Tagalog</option>
            <option value="fr">French</option>
            <option value="de">German</option>
            <option value="ja">Japanese</option>
          </select>
        </div>

        <div className="flex w-full flex-col gap-2 sm:w-auto sm:flex-row">
          <button
            onClick={onRemove}
            className="rounded-xl border border-white/10 bg-slate-800 px-4 py-2.5 text-sm font-medium text-slate-100 transition hover:border-white/20 hover:bg-slate-700"
          >
            Remove
          </button>

          {isSuccessful ? (
            <a
              href={preview}
              download={videoFile.name}
              className="inline-flex items-center justify-center rounded-xl bg-emerald-400 px-4 py-2.5 text-sm font-semibold text-slate-950 transition hover:brightness-110"
            >
              Download result
            </a>
          ) : (
            <button
              className="rounded-xl bg-cyan-400 px-4 py-2.5 text-sm font-semibold text-slate-950 shadow-lg shadow-cyan-500/20 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-70"
              onClick={handleProcess}
              disabled={isProcessing}
            >
              {isProcessing ? "Processing..." : "Process video"}
            </button>
          )}
        </div>
      </div>
    </section>
  );
}
