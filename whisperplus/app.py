import gradio as gr

from whisperplus.pipelines.whisper import SpeechToTextPipeline
from whisperplus.utils.download_utils import download_and_convert_to_mp3


def main(url, model_id, language_choice):
    """
    Main function that downloads and converts a video to MP3 format, performs speech-to-text conversion using
    a specified model, and returns the transcript along with the video path.

    Args:
        url (str): The URL of the video to download and convert.
        model_id (str): The ID of the speech-to-text model to use.
        language_choice (str): The language choice for the speech-to-text conversion.

    Returns:
        transcript (str): The transcript of the speech-to-text conversion.
        video_path (str): The path of the downloaded video.
    """
    video_path = download_and_convert_to_mp3(url)
    pipeline = SpeechToTextPipeline(model_id)
    transcript = pipeline(audio_path=video_path, model_id=model_id, language=language_choice)

    return transcript, video_path


def app():
    with gr.Blocks():
        with gr.Row():
            with gr.Column():
                youtube_url_path = gr.Text(placeholder="Enter Youtube URL", label="Youtube URL")

                language_choice = gr.Dropdown(
                    choices=[
                        "English",
                        "Turkish",
                        "Spanish",
                        "French",
                        "Chinese",
                        "Japanese",
                        "Korean",
                    ],
                    value="Turkish",
                    label="Language",
                )
                whisper_model_id = gr.Dropdown(
                    choices=[
                        "openai/whisper-large-v3",
                        "openai/whisper-large",
                        "openai/whisper-medium",
                        "openai/whisper-base",
                        "openai/whisper-small",
                        "openai/whisper-tiny",
                    ],
                    value="openai/whisper-large-v3",
                    label="Whisper Model",
                )
                whisperplus_in_predict = gr.Button(value="Generator")

            with gr.Column():
                output_text = gr.Textbox(label="Output Text")
                output_audio = gr.Audio(label="Output Audio")

        whisperplus_in_predict.click(
            fn=main,
            inputs=[
                youtube_url_path,
                whisper_model_id,
                language_choice,
            ],
            outputs=[output_text, output_audio],
        )
        gr.Examples(
            examples=[
                [
                    "https://www.youtube.com/watch?v=di3rHkEZuUw",
                    "openai/whisper-large-v3",
                    "English",
                ],
            ],
            fn=main,
            inputs=[
                youtube_url_path,
                whisper_model_id,
                language_choice,
            ],
            outputs=[output_text, output_audio],
            cache_examples=False,
        )


gradio_app = gr.Blocks()
with gradio_app:
    gr.HTML(
        """
    <h1 style='text-align: center'>
    WhisperPlus: Advancing Speech-to-Text Processing 🚀
    </h1>
    """)
    gr.HTML(
        """
        <h3 style='text-align: center'>
        Follow me for more!
        <a href='https://twitter.com/kadirnar_ai' target='_blank'>Twitter</a> | <a href='https://github.com/kadirnar' target='_blank'>Github</a> | <a href='https://www.linkedin.com/in/kadir-nar/' target='_blank'>Linkedin</a>  | <a href='https://www.huggingface.co/kadirnar/' target='_blank'>HuggingFace</a>
        </h3>
        """)
    with gr.Row():
        with gr.Column():
            app()

gradio_app.queue()
gradio_app.launch(debug=True)
