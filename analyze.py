from google.cloud import language_v1


def sample_analyze_entity_sentiment(text_content):
  """
  Analyzing Entity Sentiment in a String

  Args:
    text_content The text content to analyze
  """

  client = language_v1.LanguageServiceClient()

  # Available types: PLAIN_TEXT, HTML
  type_ = language_v1.types.Document.Type.PLAIN_TEXT

  # Optional. If not specified, the language is automatically detected.
  # For list of supported languages:
  # https://cloud.google.com/natural-language/docs/languages
  language = "en"
  document = {"content": text_content, "type_": type_, "language": language}

  # Available values: NONE, UTF8, UTF16, UTF32
  encoding_type = language_v1.EncodingType.UTF8

  response = client.analyze_entity_sentiment(
      request={"document": document, "encoding_type": encoding_type}
  )
  # Loop through entitites returned from the API
  for entity in response.entities:
    print(f"Representative name for the entity: {entity.name}")
    # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
    print(f"Entity type: {language_v1.Entity.Type(entity.type_).name}")
    # Get the salience score associated with the entity in the [0, 1.0] range
    print(f"Salience score: {entity.salience}")
    # Get the aggregate sentiment expressed for this entity in the provided document.
    sentiment = entity.sentiment
    print(f"Entity sentiment score: {sentiment.score}")
    print(f"Entity sentiment magnitude: {sentiment.magnitude}")
    print('-----------------------------------\n')
  # Loop over the metadata associated with entity. For many known entities,
    # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
    # Some entity types may have additional metadata, e.g. ADDRESS entities
    # may have metadata for the address street_name, postal_code, et al.
    for metadata_name, metadata_value in entity.metadata.items():
      print(f"{metadata_name} = {metadata_value}")

    # Loop over the mentions of this entity in the input document.
    # The API currently supports proper noun mentions.
    for mention in entity.mentions:
      print(f"Mention text: {mention.text.content}")
      # Get the mention type, e.g. PROPER for proper noun
      print(
          "Mention type: {}".format(
              language_v1.EntityMention.Type(mention.type_).name
          )
      )

  # Get the language of the text, which will be the same as
  # the language specified in the request or, if not specified,
  # the automatically-detected language.
  print(f"Language of the text: {response.language}")
  print('-----------------------------------\n')
