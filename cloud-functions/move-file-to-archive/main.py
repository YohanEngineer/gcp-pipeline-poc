from google.cloud import storage


def archive_files(event, context):
    # Set the GCS bucket name and the source and destination directories
    bucket_name = 'bucket-transit-poc'
    src_dir = ''
    dst_dir = 'archive/'

    # Connect to the GCS bucket
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    # Get a list of all the CSV files in the root directory
    blobs = bucket.list_blobs(prefix='data_')

    # Loop through the list of blobs and move each one to the destination directory
    for blob in blobs:
        # Create a new destination blob with the same name as the source blob
        destination = dst_dir + 'archived-' + blob.name
        blob_copy = bucket.copy_blob(blob, bucket, destination)
        # Delete the source blob
        blob.delete()
        print('Archiving in progress...')

    print('Archiving done!')
