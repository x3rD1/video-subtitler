interface VideoPlaceholder {
  fileName: string | null;
  videoUrl: string;
  handleRemove: () => void;
}

export default function VideoPlaceholder({
  fileName,
  videoUrl,
  handleRemove: onRemove,
}: VideoPlaceholder) {
  console.log(fileName);
  return (
    <section className="shadow rounded-lg p-4 bg-white dark:bg-gray-900">
      <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">
        {fileName}
      </p>
      <div className="aspect-video bg-black rounded overflow-hidden">
        <video src={videoUrl} controls className="w-full h-full object-cover" />
      </div>
      <div className="mt-4 flex gap-2 justify-center">
        <button onClick={onRemove} className="px-4 py-2 border rounded">
          Remove
        </button>
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded"
          onClick={() => {
            // TODO: call api process-video
          }}
        >
          Process Video
        </button>
      </div>
    </section>
  );
}
